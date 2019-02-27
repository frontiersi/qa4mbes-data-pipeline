import json
import geojson
from functools import partial

# all the geospatial libraries
from shapely import geometry, wkt
from shapely.geometry import shape
from shapely.ops import transform, cascaded_union
import pyproj


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
    return utmzone

def latlontoutm(geometry, utmzone):
    # lazily assume input geometry is latlon/EPSG:4326
    refpoint = geometry.centroid.xy
    if refpoint[1][0] > 0:
        epsgcode = 'epsg:326'+str(utmzone[2])
    else:
        epsgcode = 'epsg:327'+str(utmzone[2])
    # from: https://gis.stackexchange.com/questions/127427/transforming-shapely-polygon-and-multipolygon-objects
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),  # source coordinate system
        pyproj.Proj(init=epsgcode))  # destination coordinate system

    return transform(project, geometry)
