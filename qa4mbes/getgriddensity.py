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
import rasterio
from shapely import geometry
from shapely.geometry import shape
from shapely.ops import transform
import numpy as np

# bespoke QA4MBES
import getgridcoverage
import geotransforms


def gdaldensity(inputfile):
    """
    ASPRS las files
    """
    dataset = rasterio.open(inputfile)
    if dataset.crs:
        bbox = dataset.bounds

        xspacing = (dataset.bounds[2] - dataset.bounds[0]) / dataset.width
        yspacing = (dataset.bounds[3] - dataset.bounds[1]) / dataset.height

        # get the data boundary
        coverage = getgridcoverage.getgridcoverage(inputfile)
        coverage = shape(json.loads(coverage))

        # get the area of the coverage. first convert from WGS84 to utm
        utmzone = geotransforms.guessutm(coverage)
        utmcoverage = geotransforms.latlontoutm(coverage, utmzone)

        covered = utmcoverage.area
        mask = dataset.dataset_mask()
        datapixels = mask[mask > 0].shape[0]
        meandensity = covered/datapixels

        return json.dumps({
            'xspacing': xspacing,
            'yspacing': yspacing,
            'meandensity': meandensity,
            'area': covered,
            'npoints': datapixels
        })

    else:
        # return QA failed if there's no CRS
        return json.dumps({'QAfailed': 'No CRS present',
                           'filename': inputfile})


def getgriddensity(surveyswath):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.tif|\.TIF|\.tiff|\.bag|\.BAG$", surveyswath)):
        density = gdaldensity(surveyswath)
    else:
        print("please provide a gridded geotiff or BAG \
               file (tif/.tiff/.TIF/.TIFF/.bag/.BAG)")
        return

    return surveydensity


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input file for density extraction")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    coverage = getgriddensity(inputfile)
