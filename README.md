# qa4mbes-data-pipeline
A proof of concept of a data pipeline for quality assurance.

## Python requirements outside of the Python 3 standard library:
- shapely
- rasterio

## External software:
- MB-System: https://www.mbari.org/products/research-software/mb-system/
- PDAL: http://pdal.io


## Structure of this repository
`./doc` contains documentation as markdown
`./tests` will contain some sample data snippets and Python code to run standard tests.
`./qa4mbes` contains python code to run QA 

## instructions:

### testcoverage.py
`testcoverage` currently works for `.xyz` ungridded files swath and `.shp` reference polygons:

`python qa4mbes/testcoverage.py -i "tests/4819-100000lines.xyz" -r "tests/testcoverage.shp"`

**caveats**: other format functionality is being built. See [doc/output-template.md](the output templates) for guidance about what is returned.

XYZ files *must* be 5 tab separated columns; with the first three columns being X, Y and Z respectively (lon, lat, depth).
