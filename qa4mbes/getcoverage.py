#!/usr/bin/env python3

#standard library
import os
import json

#do we need to parse arguments...
from argparse import ArgumentParser

#additional parts
from shapely import geometry
import utm

#needs pdal
import pdal



parser = ArgumentParser()
parser.add_argument("-i", "--input-file",
                    help="input file for coverage extraction")

# unpack arguments
args = parser.parse_args()

inputfile = vars(args)["input_file"]

def mbioreadable():
    return True



def getcoverage(inputfile):
    """
    Provide a file name with extension:
    - xyz
    - las
    - laz

    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """

    pdalreader = "readers.text"

    pdalopts = ""
    #define a pipeline template
    # to do: abstract the reader block for different input file types
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
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.validate()
    pipeline.loglevel = 2 #stay quiet
    count = pipeline.execute()
    #we don't want to keep the points
    #arrays = pipeline.arrays
    #we do want the metadata...
    metadata = json.loads(pipeline.metadata)
    log = pipeline.log

    print(log)
    #print(json.dumps(metadata["stages"]["input.hexbin"]))

    """
    json_obj = pd.read_json(StringIO(metadata))['metadata']['filters.hexbin']
    wkt_boundary  = json_obj[1][u'boundary'].encode('ascii','replace')
    bbox = wkt.loads(wkt_boundary).bounds
    """
    jsonBounds=metadata["metadata"]["filters.hexbin"][0]["boundary"]
    # ...if laz/las:["metadata"]["filters.hexbin"][0]["boundary"]

    # also extract CRS

    # if no CRS exists....

    # use shapely to find polygon centroid

    # if CRS is WGS84, use utm to find the right utm zone based on centroid

    # use shapely to transform the bbox

    # ...and then estimate the density based on npoints / area (in utm)

    # ...if (MBIO readable)

    # run PDAL using hexbin boundaries with edge size ..

    #return a GeoJSON polygon
    return metadata

if __name__ == "__main__":
  getcoverage(inputfile)
