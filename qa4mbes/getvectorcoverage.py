#!/usr/bin/env python3
"""
Functions to generate JSON geometries from:
- ESRI shapefiles
- GeoJSON polygons

"""
#standard library
import os
import json
import geojson
import re

#do we need to parse arguments...
from argparse import ArgumentParser

import fiona
from shapely import geometry, wkt
from shapely.geometry import shape

def shpcoverage(inputfile):
    """
    Provide a shapefile
    Return a geometry useful to shapely
    """

    #crs = metadata["metadata"]["readers.text"][0]["srs"]["prettywkt"]
    with fiona.open(inputfile, 'r') as shapefile:
        geometry = shapefile[0]["geometry"]

    coverage = str(json.dumps(geometry))

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

def getvectorcoverage(testpolygon):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.shp$", testpolygon)):
        testcoverage = shpcoverage(testpolygon)
    elif (re.search(".*\.json$", testpolygon)):
        testcoverage = jsoncoverage(testpolygon)
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
