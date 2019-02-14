#!/usr/bin/env python3

#standard library
import os #find files
import json #do json things
import geojson #do geojson things
import re   #regexp
import datetime

#do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

#additional parts
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform

import fiona

from functools import partial
import pyproj
import utm

#bespoke QA4MBES
import getpointcoverage
import getgridcoverage
import getvectorcoverage

def transformtoutm(geometry):
    #lazily assume input geometry is latlon/EPSG:4326
    refpoint = geometry.centroid.xy
    utmzone = utm.from_latlon(refpoint[1][0], refpoint[0][0])
    if refpoint[1][0] > 0:
        epsgcode = 'epsg:326'+str(utmzone[2])
    else:
        epsgcode = 'epsg:327'+str(utmzone[2])
    # from: https://gis.stackexchange.com/questions/127427/transforming-shapely-polygon-and-multipolygon-objects
    project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:4326'), # source coordinate system
    pyproj.Proj(init=epsgcode)) # destination coordinate system

    return transform(project, geometry)

def intersectinmetres(refgeom, testgeom):
    """
    give two geometries which intersect, transform to utm,
    return area in square metres, and percent coverage
    """
    utmref = transformtoutm(refgeom)
    utmtest = transformtoutm(testgeom)

    intersection = utmref.intersection(utmtest)

    intersectionarea = intersection.area
    intersectionpercent = intersection.area / utmref.area

    return [intersectionarea, intersectionpercent]


def testcoverage(surveyswath, planningpolygon):
    """
    Given an OGR-compatible polygon and a survey swath file name, return:
    - % of reference polygon covered by survey
    - GeoJSON polygon describing intersection of reference and survey
    - distance between reference and test coverage centroids, in metres
    """

    #this may take a while, and return a...
    if (re.search(".*\.xyz$", surveyswath)):
        #returns a WKT string
        surveycoverage = getpointcoverage.xyzcoverage(surveyswath)

    elif (re.search(".*\.las|\.laz$", surveyswath)):
        #returns a wkt string
        surveycoverage = getpointcoverage.lascoverage(surveyswath)

    elif (re.search(".*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = getgridcoverage.tifcoverage(surveyswath)

    elif (re.search(".*\.bag|.BAG$", surveyswath)):
        surveycoverage = getgridcoverage.bagcoverage(surveyswath)

    # is input coverage a file or polygon? let's start at file, and choose
    # .shp or GeoJSON... return a shapely geometry
    if (re.search(".*\.shp$", planningpolygon)):
        planningcoverage = getvectorcoverage.shpcoverage(planningpolygon)

    elif (re.search(".*\.las|\.laz$", planningpolygon)):
        planningcoverage = getvectorcoverage.jsoncoverage(planningpolygon)

    # compute the intersection of the test and swath geometry

    testcentroid = planningcoverage.centroid.xy

    surveycentroid = surveycoverage.centroid.xy

    if (planningcoverage.intersects(surveycoverage)):
        #coverages intersect, compute the area of intersection
        intersects = True
        intersection = planningcoverage.intersection(surveycoverage)
        intersectionaswkt = intersection.wkt

        #intersection might be in EPSG:4326, but we want stats in metres so:
        intersectstats = intersectinmetres(planningcoverage, surveycoverage)
        #convert the intersection to a relevant UTM zone based on test poly
        intersectionarea = intersectstats[0]
        percentcoverage = intersectstats[1]

    else:
        intersects = False
        intersectionaswkt = None
        intersectionarea = None
        percentcoverage = None
    #return a dictionary, ready to write out as JSON
    testdata = {
                "testdate":datetime.datetime.now(),
                "plannedcoverage": planningpolygon,
                "testswath": surveyswath,
                "percentcovered": percentcoverage,
                "areacovered": intersectionarea,
                "coverages":{
                    "planned": {planningcoverage.wkt},
                    "swath": {surveycoverage.wkt},
                    "intersection":{intersectionaswkt}
                    }

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
