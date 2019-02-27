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

# do we need to parse arguments...
from argparse import ArgumentParser

# all the geospatial libraries
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform, cascaded_union

import rasterio
from rasterio import features

# handling BAG
import h5py
from io import BytesIO
import xml.etree.ElementTree as ET

from geotransforms import tolatlon

def parsebagmetadata(bagfile):
    #eith help fro Alex Leith
    tree = ET.parse('metadata.xml')
    root = tree.getroot()

    namespaces = {
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': "http://www.isotc211.org/2005/gco"
    }

    referencesystem = root.find('gmd:referenceSystemInfo', namespaces)[0]

    referencesystemid = reference_system.find('gmd:referenceSystemIdentifier', namespaces).find('gmd:RS_Identifier', namespaces)

    projstring = reference_system_id.find('gmd:code', namespaces).find('gco:CharacterString', namespaces).text




def tiffcoverage(inputfile):
    """
    Provide a valid geotiff file name with extension:
    -tiff/tif/TIFF/TIF
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """
    dataset = rasterio.open(inputfile)
    # check for a CRS:
    if dataset.crs:

        # this uses gdal_polygonize to draw a boundary around contiguous values
        # in the raster - we use the nodata mask so that our shapes are more or less
        # 'data' and 'nodata' regions. *assumes that the geotiff is aware of it's nodata
        # value
        boundaries = features.shapes(dataset.dataset_mask(), transform=dataset.transform)
        # assemble a list of geometries from the set of boundaries
        listofpolygons = [shape(bound[0]) for bound in boundaries]
        # create a union of all the boundaries except the last one - which so far
        # has been around the 'nodata' area but this is a bit of a risky assumption
        coverage = cascaded_union(listofpolygons[:-1])
        #crs to epsg should return an integer, so we can test equivalence to 4326
        if dataset.crs.to_epsg() != 4326:
            coverage = tolatlon(coverage, dataset.crs.to_string())

        dataset.close()

        return geojson.dumps(coverage)

    else:
        return {'QAfailed': 'No CRS present',
                'filename': inputfile}


def bagcoverage(inputfile):
    """
    Provide a valid BAG (bathymetry attributed grid) with the extension
    - .bag
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """
    # reference: https://salishsea-meopar-tools.readthedocs.io/en/latest/bathymetry/ExploringBagFiles.html
    # HDF wierdness time!

    if crsexists:
        # note CARIS BAG files encode metadata as arrays of single characters. ouch
        dataset = rasterio.open(inputfile)
        boundaries = features.shapes(dataset.dataset_mask(), transform=dataset.transform)

        coverage = geojson.dumps(cascaded_union(listofpolygons[:-1]))

        return coverage
    else:
        return {'QAfailed': 'No CRS present',
                'filename': inputfile}


def getgridcoverage(surveyswath):
    """
    function to provide a CLI app - check file extension,
    choose a coverage exractor, return a JSON coverage
    """
    if (re.search(".*\.tif|\.TIF|\.tiff$", surveyswath)):
        surveycoverage = tiffcoverage(surveyswath)
    elif (re.search(".*\.bag$", surveyswath)):
        surveycoverage = bagcoverage(surveyswath)
    else:
        print("please provide a valid geotiff or BAG file")
        return

    return surveycoverage


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input file for coverage extraction")

    # unpack arguments
    args = parser.parse_args()

    inputfile = vars(args)["input_file"]

    getgridcoverage(inputfile)
