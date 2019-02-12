#!/usr/bin/env python3
"""
Functions to generate JSON geometries from:
- ESRI shapefiles
- GeoJSON polygons

"""
#standard library
import os
import json
import re

#do we need to parse arguments...
from argparse import ArgumentParser

import fiona
import shapely

def shpcoverage(inputfile):
    """
    Provide a shapefile
    Return a geometry useful to shapely
    """

    #run PDAL
    metadata = runpdal(pipeline)
    #print(metadata)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]
    #crs = metadata["metadata"]["readers.text"][0]["srs"]["prettywkt"]

    return coverage


def jsoncoverage(inputfile):
    """
    Provide a GeoJSON file
    Return a geometry useful to shapely
    """

    #run PDAL
    metadata = runpdal(pipeline)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]

    return coverage

def getpointcoverage(surveyswath):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.shp$", surveyswath)):
        print("running xyzcoverage")
        testcoverage = xyzcoverage(surveyswath)
    elif (re.search(".*\.json$", surveyswath)):
        print("running lascoverage")
        testcoverage = lascoverage(surveyswath)
    else:
        print("please provide an ESRI shapefile or GeoJSON file")
        return

    return testcoverage


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                    help="test geometry input filename (.shp or .json)")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    getvectorcoverage(inputfile)
