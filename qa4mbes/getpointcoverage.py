#!/usr/bin/env python3
"""
Set of functions to extract data from ungridded points.

Usually using LAS/LAZ or xyz files as input.

See (TBD) for gridded coverage tooling (TIFF/BAG)

"""
#standard library
import os
import json
import re
from shapely import wkt

#do we need to parse arguments...
from argparse import ArgumentParser

#needs pdal
import pdal

def mbioreadable():
    return True

def runpdal(pipeline):
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2 #stay quiet
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

    #define a pipeline template
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
            "threshold":1
            }
        ]
        }

    #run PDAL
    metadata = runpdal(pipeline)
    #print(metadata)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]
    #crs = metadata["metadata"]["readers.text"][0]["srs"]["prettywkt"]
    #coverage = metadata
    return wkt.loads(coverage)

def lascoverage(inputfile):
    """
    Provide a file name with extension:
    - las
    - laz
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """

    #define a pipeline
    pipeline = {
        "pipeline": [
            {
            "type": "readers.las",
            "filename": inputfile
            },
            {
            "type": "filters.hexbin",
            "threshold":1
            }
        ]
        }

    #run PDAL
    metadata = runpdal(pipeline)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]

    return wkt.loads(coverage)

# ...if laz/las:["metadata"]["filters.hexbin"][0]["boundary"]

# also extract CRS

# if no CRS exists....

# use shapely to find polygon centroid

# if CRS is WGS84, use utm to find the right utm zone based on centroid

# use shapely to transform the bbox

# ...and then estimate the density based on npoints / area (in utm)

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
        print("please provide an ungridded .xyz or .las/laz file")
        return

    return surveycoverage


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                    help="input file for coverage extraction")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    coverage = getpointcoverage(inputfile)
    print(coverage)
