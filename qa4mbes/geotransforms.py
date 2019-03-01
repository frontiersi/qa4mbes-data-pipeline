import json
import geojson
from functools import partial

# all the geospatial libraries
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform, cascaded_union
import pyproj
import utm


def tolatlon(geometry, projcrs):
    """
    convert non EPSG:4326 geometries to EPSG:4326
    - needs a geometry and a proj string
    """
    project = partial(
        pyproj.transform,
        pyproj.Proj(projcrs),  # source coordinate system
        pyproj.Proj(init='epsg:4326'))  # destination coordinate system

    return transform(project, geometry)

def guessutm(geometry):
    # lazily assume input geometry is latlon/EPSG:4326
    refpoint = geometry.centroid.xy
    utmzone = utm.from_latlon(refpoint[1][0], refpoint[0][0])
    if refpoint[1][0] >= 0:
        projstring = '+proj=utm +zone='+str(utmzone[2])+' +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    else:
        projstring = '+proj=utm +zone='+str(utmzone[2])+' +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs'

    return projstring

def latlontoutm(geometry, projstring):
    # lazily assume input geometry is latlon/EPSG:4326

    # from: https://gis.stackexchange.com/questions/127427/transforming-shapely-polygon-and-multipolygon-objects
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),  # source coordinate system
        pyproj.Proj(projstring))  # destination coordinate system

    return transform(project, geometry)
