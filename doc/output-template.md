# QA4MBES output templates

JSON format test result ideas for QA4MBES.

## Survey coverage test

```
{
    'teststart': '2019-03-04T20:40:19.513322',
    'teststop': '2019-03-04T20:40:55.000691',
    'plannedcoverage': 'path/to/planned.geojson,
    'testswath': 'path/to/surveyfile.tiff',
    'percentcovered': 9.9,
    'areacovered': 9999.9999,
    'centroiddistance': 9999.9999,
    'minimumdistance': 9.9,
    'intersection': '{"type": "Polygon", "coordinates": [[[147.19636702128994, -39.24407285271974], [147.20713005294388, -39.250033916404995], [147.19802287231363, -39.27089763930338], [147.18957803209287, -39.271559979712855], [147.18245787269103, -39.25996902254708], [147.19636702128994, -39.24407285271974]]]}'
}
```

## Density test

```
{
    'teststart': '2019-03-06T09:33:50.501669',
    'teststop': '2019-03-06T09:34:13.812901',
    'testswath': 'path/to/file',
    'meandensity': 9.9999,
    'xspacing': 9.9,
    'yspacing': 9.9,
    'area': 9999.9999,
    'datapoints': 9
}
```
