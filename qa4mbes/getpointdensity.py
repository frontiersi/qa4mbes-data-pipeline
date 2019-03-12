#!/usr/bin/env python3

# standard library
import os  # find files
import json  # do json things
import geojson  # do geojson things
import re  # regexp
import datetime
import mmap

# do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

# additional parts
from shapely import geometry
from shapely.geometry import shape
from shapely.ops import transform

import pdal

# bespoke QA4MBES
import getpointcoverage
import geotransforms


def mapcount(filename):
    """
    fast line counting, from:
    https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    """
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


def runpdal(pipeline):
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2  # stay quiet
    pipeline.execute()
    metadata = json.loads(pipeline.metadata)
    pipeline.log

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

        # get the point boundary
        pointcoverage = getpointcoverage.getpointcoverage(inputfile)
        pointcoverage = shape(json.loads(pointcoverage))

        # get the area of the coverage. first convert from WGS84 to utm
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
        # return QA failed if there's no CRS
        return json.dumps({'QAfailed': 'No CRS present',
                           'filename': inputfile})


def xyzdensity(inputfile):
    """
    .xyz files (ascii point clouds or grids)
    """

    pointcoverage = getpointcoverage.getpointcoverage(inputfile)
    pointcoverage = shape(json.loads(pointcoverage))

    # get the area of the coverage. first convert from WGS84 to utm
    projstring = geotransforms.guessutm(pointcoverage)

    utmcoverage = geotransforms.latlontoutm(pointcoverage, projstring)

    covered = utmcoverage.area

    npoints = mapcount(inputfile)

    meandensity = covered/npoints

    return json.dumps({
        'meandensity': meandensity,
        'area': covered,
        'npoints': npoints
    })


def getpointdensity(surveyswath):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.xyz$", surveyswath)):
        surveydensity = xyzdensity(surveyswath)
    elif (re.search(".*\.las|\.laz$", surveyswath)):
        surveydensity = lasdensity(surveyswath)
    else:
        print("please provide an ASCII .xyz or .las/laz file")
        return

    return surveydensity


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input file for density extraction")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    coverage = getpointdensity(inputfile)
