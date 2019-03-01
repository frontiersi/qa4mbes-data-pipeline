
def getbagcrs(metadata):
    # with help from Alex Leith
    root = ET.fromstring(metadata)

    namespaces = {
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': "http://www.isotc211.org/2005/gco"
    }

    referencesystem = root.find('gmd:referenceSystemInfo', namespaces)[0]

    referencesystemid = referencesystem.find(
        'gmd:referenceSystemIdentifier', namespaces).find('gmd:RS_Identifier', namespaces)

    crswkt = referencesystemid.find('gmd:code', namespaces).find(
        'gco:CharacterString', namespaces).text

    if crswkt != '':
        crs = rasterio.crs.CRS.from_string(crswkt)
        epsgstring = rasterio.crs.CRS.to_epsg(crs)

        return epsgstring
    else:
        return False



"""
def bagcoverage(inputfile):
"""
"""
    Provide a valid BAG (bathymetry attributed grid) with the extension
    - .bag
    ...extract a tight polygon around the XY points in the file
    and return a GeoJSON polygon
    """
"""
    # reference: https://salishsea-meopar-tools.readthedocs.io/en/latest/bathymetry/ExploringBagFiles.html
    # HDF wierdness time!
    bag = h5py.File(inputfile)

    root = bag['BAG_root']
    metadata = root['metadata']

    buffer = BytesIO(metadata.value[:-1])

    metadatastring = buffer.getvalue().decode()

    crs = getbagcrs(metadatastring)

    if crs:

        thedata = root["elevation"]

        transform =

        boundaries = features.shapes(thedata, transform=transform)

        coverage = geojson.dumps(cascaded_union(listofpolygons[:-1]))

        return coverage
    else:
        return {'QAfailed': 'No CRS present',
                'filename': inputfile}
"""
