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

# bespoke QA4MBES
import getpointcoverage
import getgridcoverage
import getpointdensity
import getgriddensity

from geotransforms import guessutm, latlontoutm

# eventually the following function set could be reduced top
# 'testpdaldensity' for all PDAL readable point clouds
# ...and 'testgdaldensity' for all GDAL readable grids


def testdensity(surveyswath):
    """
    Given asurvey swath file name, return:
    - density of points for unstructured point data
    - GSD for gridded data
    - indication of whether the data and metadata match

    *Note QA always fails and no tests are run in the case of no CRS
    """

    teststart = datetime.datetime.now()

    # these functions should all return GeoJSON polygons or multipolygons
    if (re.search(".*\.xyz$", surveyswath)):
        density = getpointdensity.xyzdensity(surveyswath)
    # not tested yet
    elif (re.search(".*\.las|\.laz$", surveyswath)):
        density = getpointdensity.lasdensity(surveyswath)
    # building now
    elif (re.search(".*\.tif|\.TIF|\.tiff|\.bag|\.BAG$", surveyswath)):
        density = getgriddensity.gdaldensity(surveyswath)

    # if survey coverage or planning coverage doesn't have a CRS:
    if density.find("QAfailed") > -1:
        return density

    else:
        if density.find('xspacing') > -1:
            density = json.loads(density)
            meandensity = density["meandensity"]
            xspacing = density["xspacing"]
            yspacing = density["yspacing"]
            npoints = density["npoints"]
            area = density["area"]
        else:
            density = json.loads(density)
            meandensity = density["meandensity"]
            xspacing = None
            yspacing = None
            npoints = density["npoints"]
            area = density["area"]

    teststop = datetime.datetime.now()

    # return a dictionary, ready to write out as JSON
    testdata = {
        "teststart": str(teststart.isoformat()),
        "teststop": str(teststop.isoformat()),
        "testswath": surveyswath,
        "meandensity": meandensity,
        "xspacing": xspacing,
        "yspacing": yspacing,
        "area": area,
        "datapoints": npoints
    }

    return testdata


if __name__ == "__main__":
    # cli handling parts -
    # accept a test and reference polygon
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input filename for coverage extraction")

    # input CRS for each should also nbe options... coming!

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    density = testdensity(inputfile)

    print(density)
