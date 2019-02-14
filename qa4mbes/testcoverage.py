#!/usr/bin/env python3

#standard library
import os #find files
import json #do json things
import re   #regexp

#do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

#additional parts
from shapely import geometry
import fiona

#bespoke QA4MBES
import getpointcoverage
import getgridcoverage
import shapelyify


def intersectiontest():


    return


def testcoverage(surveyswath, planningpolygon):
    """
    Given an OGR-compatible polygon and a survey swath file name, return:
    - % of reference polygon covered by survey
    - GeoJSON polygon describing intersection of reference and survey
    - distance between reference and test coverage centroids, in metres
    """

    #this may take a while, and return a...
    if (re.search("*\.xyz$", surveyswath)):
        #returns a WKT string
        surveycoverage = getpointcoverage.xyzcoverage(surveyswath)

    elif (re.search("*\.las|\.laz$", surveyswath)):
        #returns a wkt string
        surveycoverage = getpointcoverage.lascoverage(surveyswath)

    elif (re.search("*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = getgridcoverage.tifcoverage(surveyswath)

    else (re.search("*\.bag|.BAG$", surveyswath)):
        surveycoverage = getgridcoverage.bagcoverage(surveyswath)

    #create a shapely geometry from the returned survey coverage JSON
    surveygeometry = shapelyify(surveycoverage)

    # is input coverage a file or polygon? let's start at file, and choose
    # .shp or GeoJSON... return a shapely geometry
    if (re.search("*\.shp$", planningpolygon)):
        planningcoverage = getvectorcoverage.getshp(planningpolygon)

    elif (re.search("*\.las|\.laz$", planningpolygon)):
        planningcoverage = getvectorcoverage.getjson(planningpolygon)

    # compute the intersection of the test and swath geometry

    testcentroid = planningcoverage.centroid()

    surveycentroid = surveycoverage.centroid()

    if (planningcoverage.intersects(surveycoverage)):
        #coverages intersect, compute the area of intersection
        intersects = True
        intersection =
    else:
        intersects = False
        intersection = None
        intersectionarea = None



    #return a dictionary, ready to write out as JSON
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
    referencepolygon = vars(args)["referencpolygon"]

    testdata = testcoverage(inputfile, referencepolygon)
    # spit JSON to stdout as a CLI output
    print(testdata)
