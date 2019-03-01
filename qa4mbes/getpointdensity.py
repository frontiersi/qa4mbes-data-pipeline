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

import pdal

from functools import partial
import pyproj
import utm

# bespoke QA4MBES
import getpointcoverage
import geotransforms

def runpdal(pipeline):
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2  # stay quiet
    count = pipeline.execute()
    metadata = json.loads(pipeline.metadata)
    log = pipeline.log

    return metadata

def lasdensity(inputfile):
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
        pointcoverage = getpointcoverage.getpointcoverage(inputfile)
        pointcoverage = shape(json.loads(pointcoverage))

        ## get the area of the coverage. first convert from WGS84 to utm
        utmzone = geotransforms.guessutm(pointcoverage)
        utmcoverage = geotransforms.latlontoutm(pointcoverage, utmzone)

        covered = utmcoverage.area

        npoints = metadata["metadata"]["readers.las"][0]["count"]

        meandensity = covered/npoints

        return json.dumps({
                            'meandensity': meandensity,
                            'area': covered,
                            'npoints': npoints
        })
    else:
        return json.dumps({'QAfailed': 'No CRS present',
                'filename': inputfile})


def xyzdensity(inputfile):
    """
    .xyz files (ascii point clouds or grids)
    use PDAL because... its fast
    """

    pointcoverage = getpointcoverage.getpointcoverage(inputfile)
    pointcoverage = shape(json.loads(pointcoverage))

    ## get the area of the coverage. first convert from WGS84 to utm
    projstring= geotransforms.guessutm(pointcoverage)
    print(projstring)
    utmcoverage = geotransforms.latlontoutm(pointcoverage, projstring)

    # define a pipeline
    metapipeline = {
        "pipeline": [
            {
                "type": "readers.text",
                "header": "X\tY\tZ\tFlightllineID\tIntensity",
                "spatialreference": "EPSG:4326",
                "filename": inputfile
            },
            {
            "type": "filters.reprojection",
            "in_srs": "EPSG:4326",
            "out_srs": projstring
            }
        ]
    }
    metadata = runpdal(metapipeline)

    return metadata
