#!/usr/bin/env python3

#standard library
import os
import json
import re

#do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

#additional parts
from shapely import geometry

#bespoke QA4MBES
import getcoverage


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


def testcoverage(planningpolygon, surveyswath):
    """
    Given an OGR-compatible polygon and a survey swath file name, return:
    - % of reference polygon covered by survey
    - GeoJSON polygon describing intersection of reference and survey
    - distance between reference and test coverage centroids, in metres
    """

    #this may take a while
    if (re.search("*\.xyz$", surveyswath)):
        surveycoverage = getcoverage.xyzcoverage(surveyswath)

    elif (re.search("*\.las|\.laz$", surveyswath)):
        surveycoverage = getcoverage.lascoverage(surveyswath)

    elif (re.search("*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = getcoverage.tifcoverage(surveyswath)

    else (re.search("*\.bag|.BAG$", surveyswath)):
        surveycoverage = getcoverage.bagcoverage(surveyswath)

    #return a dictionary, ready to write out as JSON
    return testdata



if __name__ == "__main__":
  testcoverage(reference, test)
