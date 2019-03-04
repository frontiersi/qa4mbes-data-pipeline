#!/usr/bin/env python3
"""
Set of functions to extract data from ungridded points.

Usually using LAS/LAZ or xyz files as input.

See (TBD) for gridded coverage tooling (TIFF/BAG)

"""
# standard library
import os
import json
import geojson
import re
from functools import partial

# do we need to parse arguments...yes!
from argparse import ArgumentParser

# needs pdal and shapely and pyproj
import pdal
from shapely import wkt
from shapely.ops import transform
import pyproj

# qa4mbes parts

from geotransforms import tolatlon


def runpdal(pipeline):
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2  # stay quiet
    count = pipeline.execute()
    metadata = json.loads(pipeline.metadata)
    log = pipeline.log

    return metadata


def xyzcoverage(inputfile):
    """
    Provide a file name with extension:
    - xyz
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """

    # define a pipeline template
    # to do: inspect the data format from line 1
    # of the input file and construct 'header' appropriately
    # OR take a header argument...
    pipeline = {
        "pipeline": [
            {
                "type": "readers.text",
                "header": "X\tY\tZ\tFlightllineID\tIntensity",
                "spatialreference": "EPSG:4326",
                "filename": inputfile
            },
            {
                "type": "filters.hexbin",
                "threshold": 1
            }
        ]
    }

    # run PDAL
    metadata = runpdal(pipeline)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]
    # print(metadata)

    # gymnastics to convert from PDAL wkt to geoJSON
    coverage = wkt.loads(metadata["metadata"]["filters.hexbin"][0]["boundary"])
    coverage = geojson.dumps(coverage)

    return coverage


def lascoverage(inputfile):
    """
    Provide a file name with extension:
    - las
    - laz
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """

    # define a pipeline
    metapipeline = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": inputfile
            }
        ]
    }

    metadata = runpdal(metapipeline)

    if metadata["metadata"]["readers.las"][0]["srs"]["proj4"]:

        srsprojstring = metadata["metadata"]["readers.las"][0]["srs"]["proj4"]

        boundspipeline = {
            "pipeline": [
                {
                    "type": "readers.las",
                    "filename": inputfile
                },
                {
                    "type": "filters.hexbin",
                    "threshold": 1
                }
            ]
        }

        # run PDAL
        metadata = runpdal(boundspipeline)

        # gymnastics to convert from PDAL wkt to geoJSON
        coverage = wkt.loads(metadata["metadata"]["filters.hexbin"][0]["boundary"])

        # if the coverage is not WGS84 lat/lon:
        if srsprojstring.find('longlat') < 0:

            coverage = tolatlon(coverage, srsprojstring)

        coverage = geojson.dumps(coverage)

        return coverage
    else:
        return json.dumps({'QAfailed': 'No CRS present',
                           'filename': inputfile})


def getpointcoverage(surveyswath):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.xyz$", surveyswath)):
        #print("running xyzcoverage")
        surveycoverage = xyzcoverage(surveyswath)
    elif (re.search(".*\.las|\.laz$", surveyswath)):
        #print("running lascoverage")
        surveycoverage = lascoverage(surveyswath)
    else:
        print("please provide an ASCII .xyz or .las/laz file")
        return

    return surveycoverage


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input file for coverage extraction")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    getpointcoverage(inputfile)
