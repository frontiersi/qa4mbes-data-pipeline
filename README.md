# qa4mbes-data-pipeline
A proof of concept of a data pipeline for quality assurance.

## Python requirements outside of the Python 3 standard library:
- shapely
- rasterio
- pdal (http://pdal.io)

## External software not used as a Python library
- MB-System: https://www.mbari.org/products/research-software/mb-system/

## Structure of this repository
`./doc` contains documentation as markdown
`./tests` will contain some sample data snippets and Python code to run standard tests.
`./qa4mbes` contains python code to run QA
`./notebooks` contains Jupyter notebooks with usage examples for each tool

## Instructions:

### testcoverage.py
Assess whether a survey covers a planned region [more...](./doc/testcoverage.md)

### testresolution.py
Assess the resolution of a survey [more...]

### testgridresolution.py
Assess the resolution of gridded data files [more...]
