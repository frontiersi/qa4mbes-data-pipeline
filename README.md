# qa4mbes-data-pipeline
A proof of concept of a data pipeline for quality assurance.

## Python requirements outside of the Python 3 standard library:

- pdal (http://pdal.io)
- pyproj
- shapely
- rasterio
- utm

See [environment.yml](./environment.yml) for the conda environment setup used to run the code here. A [requirements.txt](./doc/requirements.txt) file is also available.

## Structure of this repository
`./doc` contains documentation as markdown  
`./tests` will contain some sample data snippets and Python code to run standard tests.  
`./qa4mbes` contains python code to run QA  
`./notebooks` contains Jupyter notebooks with usage examples for each tool  

## Instructions:

### testcoverage.py
Assess whether a survey covers a planned region [more...](./doc/testcoverage.md)

### testdensity.py
Assess the density of a survey [more...](./doc/testdensity.md)

# Docker instructions
* Build: `docker-compose build`
* Run example 1:
```
docker-compose run qa4mbes \
    python3 qa4mbes/testcoverage.py \
    -i "tests/xyzdata/4819-100000lines.xyz" \
    -r "tests/gridcoverages/testcoverage.shp"
```
* Run example 2:
```
docker-compose run qa4mbes \
    python3 qa4mbes/testdensity.py \
    -i "tests/xyzdata/4819-100000lines.xyz"
```

## Jupyter from Docker
Run the Jupyter notebooks within Docker:

```
    docker-compose up qa4mbes
```

Jupyter will be accessible from [http://localhost:8888/?token=<ACCESS_TOKEN_FROM_DOCKER_UP_CMD>](http://localhost:8888/)
