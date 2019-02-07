#!/usr/bin/env python3

#standard library
import os
import json

#do we need to parse arguments...
# yes! if we're calling from the CLI
from argparse import ArgumentParser

#additional parts
from shapely import geometry

#bespoke QA4MBES
import getcoverage


def testcoverage(planningpolygon, surveyswath):
    """
    Given an OGR-compatible polygon and a survey swath, return:
    - % of reference polygon covered by survey
    - GeoJSON polygon describing intersection of reference and survey
    - distance between reference and test coverage centroids, in metres
    """

    #this may take a while
    surveycoverage = getcoverage(surveyswath)


    #return a dictionary, ready to write out as JSON
    return testdata



if __name__ == "__main__":
  testcoverage(reference, test)
