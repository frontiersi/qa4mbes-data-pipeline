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

from functools import partial
import pyproj
import utm

def runpdal(pipeline):
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2  # stay quiet
    count = pipeline.execute()
    metadata = json.loads(pipeline.metadata)
    log = pipeline.log

    return metadata

def getlasdensity(inputfile):
    """
    ASPRS las files
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

        ## get the point boundary
        pointcoverage = getpointcoverage(inputfile)

        ## get the area of the coverage
        covered = pointcoverage.area()
        npoints = metadata["metadata"]["readers.las"][0]["count"]

        meandensity = npoints/covered

        return meandensity
    else:
        return json.dumps({'QAfailed': 'No CRS present',
                'filename': inputfile})


def getxyzdensity(inputfile):
    """
    .xyz files (ascii point clouds or grids)
    """
