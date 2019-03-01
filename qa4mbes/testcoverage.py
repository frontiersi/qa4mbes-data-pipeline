#!/usr/bin/env python3

# standard library
import os  # find files
import json  # do json things
import geojson  # do geojson things
import re  # regexp
import datetime

# do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

# additional parts
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform

import fiona

from functools import partial
import pyproj
import utm

# bespoke QA4MBES
import getvectorcoverage
import getpointcoverage
import getgridcoverage

from geotransforms import guessutm, latlontoutm

def intersectinmetres(refgeom, testgeom):
    """
    give two geometries which intersect
    return area in geometry units, and percent coverage
    """
    intersection = refgeom.intersection(testgeom)

    intersectionarea = intersection.area
    intersectionpercent = intersection.area / refgeom.area

    return [intersectionarea, intersectionpercent]


def jsontoshapely(coverage):
    """
    give a valid GeoJSON object, return a shapely geometry
    """
    coverage = geojson.loads(coverage)
    return shape(coverage)


def testcoverage(surveyswath, planningpolygon):
    """
    Given an OGR-compatible polygon and a survey swath file name, return:
    - percentage of reference polygon covered by survey
    - GeoJSON polygon describing intersection of reference and survey
    - distance between reference and test coverage centroids, in metres
    """

    teststart = datetime.datetime.now()

    # fail fast - load coverage and check for CRS
    # is input coverage a file or polygon? let's start at file, and choose
    # .shp or GeoJSON... return a shapely geometry
    if (re.search(".*\.shp$", planningpolygon)):
        planningcoverage = getvectorcoverage.shpcoverage(planningpolygon)

    elif (re.search(".*\.json|\.geojson$", planningpolygon)):
        planningcoverage = getvectorcoverage.jsoncoverage(planningpolygon)

        #if survey coverage or planning coverage doesn't have a CRS:
    if planningcoverage.find("QAfailed") > 0:
        return planningcoverage

    # these functions should all return GeoJSON polygons or multipolygons
    if (re.search(".*\.xyz$", surveyswath)):
        surveycoverage = getpointcoverage.xyzcoverage(surveyswath)

    elif (re.search(".*\.las|\.laz$", surveyswath)):
        surveycoverage = getpointcoverage.lascoverage(surveyswath)

    elif (re.search(".*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = getgridcoverage.gdalcoverage(surveyswath)

    elif (re.search(".*\.bag|.BAG$", surveyswath)):
        surveycoverage = getgridcoverage.gdalcoverage(surveyswath)

    #if survey coverage or planning coverage doesn't have a CRS:
    if surveycoverage.find("QAfailed") > 0:
        return surveycoverage

    #if there are no QA issues already, proceed:
    else:

        # create shapely geometries from geoJSON coverages
        planningcoverage = jsontoshapely(planningcoverage)
        surveycoverage = jsontoshapely(surveycoverage)

        utmzone = guessutm(planningcoverage)

        # convert to a relevant UTM zone based on test poly
        utmplanned = latlontoutm(planningcoverage, utmzone)
        utmsurvey = latlontoutm(surveycoverage, utmzone)

        # compute centroid distance in metres regardless of intersection
        centroiddistance = utmplanned.centroid.distance(utmsurvey.centroid)
        minimumdistance = utmplanned.distance(utmsurvey)

        if (planningcoverage.intersects(surveycoverage)):
            # coverages intersect, compute the area of intersection
            intersects = True
            intersection = planningcoverage.intersection(surveycoverage)
            #intersectionaswkt = intersection.wkt
            intersectionasjson = geojson.dumps(intersection)

            # intersection might be in EPSG:4326, but we want stats in metres so:
            intersectstats = intersectinmetres(utmplanned, utmsurvey)

            intersectionarea = intersectstats[0]
            percentcoverage = intersectstats[1]

        else:
            intersects = False
            intersectionasjson = None
            intersectionarea = None
            percentcoverage = None

        teststop = datetime.datetime.now()
        # return a dictionary, ready to write out as JSON
        testdata = {
            "teststart": str(teststart.isoformat()),
            "teststop": str(teststop.isoformat()),
            "plannedcoverage": planningpolygon,
            "testswath": surveyswath,
            "percentcovered": percentcoverage,
            "areacovered": intersectionarea,
            "centroiddistance": centroiddistance,
            "minimumdistance": minimumdistance,
            "intersection": intersectionasjson
        }

        return testdata


if __name__ == "__main__":
    # cli handling parts -
    # accept a test and reference polygon
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input filename for coverage extraction")

    parser.add_argument("-r", "--referencepolygon",
                        help="refernce polygon filename")

    # input CRS for each should also nbe options... coming!

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]
    referencepolygon = vars(args)["referencepolygon"]

    testdata = testcoverage(inputfile, referencepolygon)
    # spit JSON to stdout as a CLI output
    print(testdata)
