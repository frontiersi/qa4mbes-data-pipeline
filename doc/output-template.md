# QA4MBES output templates

JSON format test result ideas for QA4MBES.

- Polygons should be GeoJSON
- Output should carry close compatibility with STAC-spec

## Survey coverage test

```
{
  "testdate": "unixdatetimestamp",
  "plannedcoverage": filename,
  "inputswath": "filename",
  "percentcovered": 99.5 (or None),
  "areacovered": 99999 (or None),
  "coverage": {
    "planned": {geoJSON polygon}.

    "swath": {geoJSON polygon or multiploygon},

    "intersection": {geoJSON polygon or None}
    }
}
```

## Density test

```
{
  "testdate": "unixdatetimestamp",
  "inputswath": "file.ascii",
  "swatharea": 999999.99,
  "points": 99999,
  "meandensity": 99.99,
  "coverage": {
    "swath": {geoJSON polygon or multiploygon},
    }
}
```
