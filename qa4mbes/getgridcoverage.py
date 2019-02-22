#!/usr/bin/env python3
"""
Set of functions to extract data from ungridded points.

Usually using LAS/LAZ or xyz files as input.

See (TBD) for gridded coverage tooling (TIFF/BAG)

"""
# standard library
import os
import json
import re

# do we need to parse arguments...
from argparse import ArgumentParser

# all the geospatial libraries
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform, cascaded_union

import rasterio
from rasterio import features

import pdal


def xyzcoverage(inputfile, header="X\tY\t\Z\tFlightllineID\tIntensity"):
    """
    Provide a delimited ASCII file with at least X Y and Z coordinates

    Optionally provide a header line for the input data schema
    ...and a CRS as EPSG code

    ...extract a tight polygon around data points in the file
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
                "header": header,
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
    # print(metadata)
    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]
    #crs = metadata["metadata"]["readers.text"][0]["srs"]["prettywkt"]

    return coverage


def tiffcoverage(inputfile):
    """
    Provide a valid geotiff file name with extension:
    -tiff/tif/TIFF/TIF
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon

    """
    dataset = rasterio.open(inputfile)
    boundaries = features.shapes(dataset.dataset_mask(), transform=dataset.transform)
    multipoly = cascaded_union(listofpolygons[:-1])

    coverage = metadata["metadata"]["filters.hexbin"][0]["boundary"]

    return coverage

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
        print("running xyzcoverage")
        surveycoverage = xyzcoverage(surveyswath)
    elif (re.search(".*\.las|\.laz$", surveyswath)):
        print("running lascoverage")
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

    getpointcoverage(inputfile)
