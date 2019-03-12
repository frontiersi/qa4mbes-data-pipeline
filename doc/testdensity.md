## Running density tests

`testdensity` checks the point density (points per square unit) of a dataset. If the dataset is gridded, it also checks the grid spacing. It returns:

- test start time
- test stop time
- test swath file name
- mean data point density in points-per-unit (usually metres)
- X grid spacing
- Y grid spacing
- area of a tight bounding box around the data
- number of data points or pixels.

As for `testcoverage.py`, the test will fail if the input data should hold CRS metadata but do not (eg LAS, geoTIFF or BAG file formats)

`testdensity.py` currently works for `.xyz` and `las/laz` ungridded swath files and `.tiff` or `.bag` gridded files:

`python qa4mbes/testdensity.py -i "tests/xyzdata/4819-100000lines.xyz"`

### Caveats

- XYZ files *must* have 5 tab separated columns; with the first three columns being X, Y and Z respectively (lon, lat, depth).
- output geometries are always expressed in `EPSG:4326` (latitude, longitude)
- input `geoJSON` and `.xyz` files are **always** assumed to contain coordinates expressed in `EPSG:4326` (lat/lon).

### Examples:

See the [notebook example for all data types](../notebooks/densitytesting.ipynb)
