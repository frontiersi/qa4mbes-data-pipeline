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


def testcoverage(surveyswath):
    """
    Given asurvey swath file name, return:
    - density of points for unstructred point data
    - GSD for gridded data
    - indication of whether the data and metadata match

    *Note QA always fails and no tests are run in the case of no CRS
    """

    teststart = datetime.datetime.now()

    # these functions should all return GeoJSON polygons or multipolygons
    if (re.search(".*\.xyz$", surveyswath)):
        surveycoverage = getpointcoverage.getpointcoverage(surveyswath)
    # not tested yet
    elif (re.search(".*\.las|\.laz$", surveyswath)):
        surveycoverage = getpointcoverage.lascoverage(surveyswath)
    # building now
    elif (re.search(".*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = getgridcoverage.tiffcoverage(surveyswath)

    # queued
    elif (re.search(".*\.bag|.BAG$", surveyswath)):
        surveycoverage = getgridcoverage.bagcoverage(surveyswath)

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
