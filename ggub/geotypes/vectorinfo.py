import sys
from osgeo import gdal
from osgeo import ogr

bReadOnly = False
bVerbose = True
bSummaryOnly = False
nFetchFID = ogr.NullFID
papszOptions = None


def string_equal(a, b):
    return a.lower() == b.lower()


def get_info(datasource, full_report=True):

    global bReadOnly
    global bVerbose
    global bSummaryOnly
    global nFetchFID
    global papszOptions

    where_clause = None
    # datasource = None
    layers = None
    spatial_filter = None
    repeat_count = 1
    all_layers = False
    sql_statement = None
    dialect = None
    options = {}
    geom_field = None

    info = {}

#     if argv is None:
#         argv = sys.argv
#
#     argv = ogr.GeneralCmdLineProcessor( argv )
#
# # --------------------------------------------------------------------
# #      Processing command line arguments.
# # --------------------------------------------------------------------
#     if argv is None:
#         return 1
#
#     nArgc = len(argv)
#
#     iArg = 1
#     while iArg < nArgc:
#
#         if string_equal(argv[iArg], "--utility_version"):
#             print("%s is running against GDAL %s" %
#                    (argv[0], gdal.VersionInfo("RELEASE_NAME")))
#             return 0
#
#         elif string_equal(argv[iArg], "-ro"):
#             bReadOnly = True
#         elif string_equal(argv[iArg], "-q") or string_equal(argv[iArg], "-quiet"):
#             bVerbose = False
#         elif string_equal(argv[iArg], "-fid") and iArg < nArgc-1:
#             iArg = iArg + 1
#             nFetchFID = int(argv[iArg])
#         elif string_equal(argv[iArg], "-spat") and iArg + 4 < nArgc:
#             oRing = ogr.Geometry(ogr.wkbLinearRing)
#
#             oRing.AddPoint( float(argv[iArg+1]), float(argv[iArg+2]) )
#             oRing.AddPoint( float(argv[iArg+1]), float(argv[iArg+4]) )
#             oRing.AddPoint( float(argv[iArg+3]), float(argv[iArg+4]) )
#             oRing.AddPoint( float(argv[iArg+3]), float(argv[iArg+2]) )
#             oRing.AddPoint( float(argv[iArg+1]), float(argv[iArg+2]) )
#
#             spatial_filter = ogr.Geometry(ogr.wkbPolygon)
#             spatial_filter.AddGeometry(oRing)
#             iArg = iArg + 4
#
#         elif string_equal(argv[iArg], "-geomfield") and iArg < nArgc-1:
#             iArg = iArg + 1
#             geom_field = argv[iArg]
#
#         elif string_equal(argv[iArg], "-where") and iArg < nArgc-1:
#             iArg = iArg + 1
#             where_clause = argv[iArg]
#
#         elif string_equal(argv[iArg], "-sql") and iArg < nArgc-1:
#             iArg = iArg + 1
#             sql_statement = argv[iArg]
#
#         elif string_equal(argv[iArg], "-dialect") and iArg < nArgc-1:
#             iArg = iArg + 1
#             dialect = argv[iArg]
#
#         elif string_equal(argv[iArg], "-rc") and iArg < nArgc-1:
#             iArg = iArg + 1
#             repeat_count = int(argv[iArg])
#
#         elif string_equal(argv[iArg], "-al"):
#             all_layers = True
#
#         elif string_equal(argv[iArg], "-so") or string_equal(argv[iArg], "-summary"):
#             bSummaryOnly = True
#
#         elif len(argv[iArg]) > 8 and string_equal(argv[iArg][0:8], "-fields="):
#             options['DISPLAY_FIELDS'] = argv[iArg][7:len(argv[iArg])]
#
#         elif len(argv[iArg]) > 6 and string_equal(argv[iArg][0:6], "-geom="):
#             options['DISPLAY_GEOMETRY'] = argv[iArg][6:len(argv[iArg])]
#
#         elif argv[iArg][0] == '-':
#             return Usage()
#
#         elif datasource is None:
#             datasource = argv[iArg]
#         else:
#             if layers is None:
#                 layers = []
#             layers.append( argv[iArg] )
#             all_layers = False
#
#         iArg = iArg + 1
#
#     if datasource is None:
#         return Usage()

    # Open data source.


    dataset = None
    driver = None

    dataset = ogr.Open(datasource, True)  # ReadOnly
    # dataset = ogr.Open(datasource, not bReadOnly)
    # if dataset is None and not bReadOnly:
    #     dataset = ogr.Open(datasource, False)
    #     if dataset is not None and bVerbose:
    #         print( "Had to open data source read-only." )
    #         bReadOnly = True

# --------------------------------------------------------------------
#      Report failure.
# --------------------------------------------------------------------
    if dataset is None:
        drivers = [ogr.GetDriver(iDriver).GetName() for iDriver in range(ogr.GetDriverCount())]
        info["Error"] = f"Unable to open datasource {datasource} with the following drivers: {drivers}"
        # print( "FAILURE:\n"
        #         "Unable to open datasource `%s' with the following drivers." % datasource )
        #
        # for iDriver in range(ogr.GetDriverCount()):
        #     print( "  -> %s" % ogr.GetDriver(iDriver).GetName() )
        #
        # return 1
        return info

    driver = dataset.GetDriver()

# # --------------------------------------------------------------------
# #      Some information messages.
# # --------------------------------------------------------------------
#     if bVerbose:
#         print( "INFO: Open of `%s'\n"
#                 "      using driver `%s' successful." % (datasource, driver.GetName()) )

    ds_name = dataset.GetName()
    if str(type(datasource)) == "<type 'unicode'>" and str(type(ds_name)) == "<type 'str'>":
        ds_name = ds_name.decode("utf8")
    if datasource != ds_name:
        info["NameInfo"] = f"Internal data source name {ds_name} is different from user name {datasource}"
    # if bVerbose and datasource != ds_name:
    #     print( "INFO: Internal data source name `%s'\n"
    #             "      different from user name `%s'." % (ds_name, datasource ))

# --------------------------------------------------------------------
#      Special case for -sql clause.  No source layers required.
# --------------------------------------------------------------------
#     if sql_statement is not None:
#         poResultSet = None
#
#         repeat_count = 0  #// skip layer reporting.
#
#         if layers is not None:
#             print( "layer names ignored in combination with -sql." )
#
#         if geom_field is None:
#             poResultSet = dataset.ExecuteSQL( sql_statement, spatial_filter,
#                                             dialect )
#         else:
#             poResultSet = dataset.ExecuteSQL( sql_statement, None, dialect )
#
#         if poResultSet is not None:
#             if where_clause is not None:
#                 if poResultSet.SetAttributeFilter( where_clause ) != 0:
#                     print("FAILURE: SetAttributeFilter(%s) failed." % where_clause)
#                     return 1
#
#             if geom_field is not None:
#                 ReportOnLayer( poResultSet, None, geom_field, spatial_filter, options )
#             else:
#                 ReportOnLayer( poResultSet, None, None, None, options )
#             dataset.ReleaseResultSet( poResultSet )
#
#     #gdal.Debug( "OGR", "GetLayerCount() = %d\n", dataset.GetLayerCount() )
#
    for iRepeat in range(repeat_count):
        if layers is None:
# --------------------------------------------------------------------
#      Process each data source layer.
# --------------------------------------------------------------------
            for iLayer in range(dataset.GetLayerCount()):
                poLayer = dataset.GetLayer(iLayer)

                if poLayer is None:
                    print( "FAILURE: Couldn't fetch advertised layer %d!" % iLayer )
                    return 1

                if not all_layers:
                    line = "%d: %s" % (iLayer+1, poLayer.GetLayerDefn().GetName())

                    nGeomFieldCount = poLayer.GetLayerDefn().GetGeomFieldCount()
                    if nGeomFieldCount > 1:
                        line = line + " ("
                        for iGeom in range(nGeomFieldCount):
                            if iGeom > 0:
                                line = line + ", "
                            poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                            line = line + "%s" % ogr.GeometryTypeToName( poGFldDefn.GetType() )
                        line = line + ")"

                    if poLayer.GetLayerDefn().GetGeomType() != ogr.wkbUnknown:
                        line = line + " (%s)" % ogr.GeometryTypeToName( poLayer.GetLayerDefn().GetGeomType() )

                    print(line)
                else:
                    if iRepeat != 0:
                        poLayer.ResetReading()

                    info[str(iLayer)] = ReportOnLayer( poLayer, where_clause, geom_field, spatial_filter, options )

        else:
# --------------------------------------------------------------------
#      Process specified data source layers.
# --------------------------------------------------------------------
            for papszIter in layers:
                poLayer = dataset.GetLayerByName(papszIter)

                if poLayer is None:
                    print( "FAILURE: Couldn't fetch requested layer %s!" % papszIter )
                    return 1

                if iRepeat != 0:
                    poLayer.ResetReading()

                ReportOnLayer( poLayer, where_clause, geom_field, spatial_filter, options )

# --------------------------------------------------------------------
#      Close down.
# --------------------------------------------------------------------
    dataset.Destroy()

    return 0

#**********************************************************************
#                               Usage()
#**********************************************************************

# def Usage():
#
#     print( "Usage: ogrinfo [--help-general] [-ro] [-q] [-where restricted_where]\n"
#             "               [-spat xmin ymin xmax ymax] [-geomfield field] [-fid fid]\n"
#             "               [-sql statement] [-al] [-so] [-fields={YES/NO}]\n"
#             "               [-geom={YES/NO/SUMMARY}][--formats]\n"
#             "               datasource_name [layer [layer ...]]")
#     return 1

#**********************************************************************
#                           ReportOnLayer()
#**********************************************************************

def ReportOnLayer( poLayer, pszWHERE, pszGeomField, poSpatialFilter, options ):

    lyr_info = {}

    poDefn = poLayer.GetLayerDefn()

# --------------------------------------------------------------------
#      Set filters if provided.
# --------------------------------------------------------------------
#     if pszWHERE is not None:
#         if poLayer.SetAttributeFilter( pszWHERE ) != 0:
#             print("FAILURE: SetAttributeFilter(%s) failed." % pszWHERE)
#             return

    # if poSpatialFilter is not None:
    #     if pszGeomField is not None:
    #         iGeomField = poLayer.GetLayerDefn().GetGeomFieldIndex(pszGeomField)
    #         if iGeomField >= 0:
    #             poLayer.SetSpatialFilter( iGeomField, poSpatialFilter )
    #         else:
    #             print("WARNING: Cannot find geometry field %s." % pszGeomField)
    #     else:
    #         poLayer.SetSpatialFilter( poSpatialFilter )

# --------------------------------------------------------------------
#      Report various overall information.
# --------------------------------------------------------------------
    print( "" )

    print( "Layer name: %s" % poDefn.GetName() )

    lyr_info["Name"] = poDefn.GetName()

    if bVerbose:
        nGeomFieldCount = poLayer.GetLayerDefn().GetGeomFieldCount()
        if nGeomFieldCount > 1:
            for iGeom in range(nGeomFieldCount):
                poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                print( "Geometry (%s): %s" % (poGFldDefn.GetNameRef(), ogr.GeometryTypeToName( poGFldDefn.GetType() ) ))
        else:
            print( "Geometry: %s" % ogr.GeometryTypeToName( poDefn.GetGeomType() ) )

        lyr_info["Geometry"] = ogr.GeometryTypeToName(poDefn.GetGeomType())

        print( "Feature Count: %d" % poLayer.GetFeatureCount() )

        lyr_info["Feature Count"] = poLayer.GetFeatureCount()

        return lyr_info

        if nGeomFieldCount > 1:
            for iGeom in range(nGeomFieldCount):
                poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                oExt = poLayer.GetExtent(True, geom_field = iGeom, can_return_null = True)
                if oExt is not None:
                    print("Extent (%s): (%f, %f) - (%f, %f)" % (poGFldDefn.GetNameRef(), oExt[0], oExt[2], oExt[1], oExt[3]))
        else:
            oExt = poLayer.GetExtent(True, can_return_null = True)
            if oExt is not None:
                print("Extent: (%f, %f) - (%f, %f)" % (oExt[0], oExt[2], oExt[1], oExt[3]))

        if nGeomFieldCount > 1:
            for iGeom in range(nGeomFieldCount):
                poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                if poGFldDefn.GetSpatialRef() is None:
                    pszWKT = "(unknown)"
                else:
                    pszWKT = poGFldDefn.GetSpatialRef().ExportToPrettyWkt()
                print( "SRS WKT (%s):\n%s" % (poGFldDefn.GetNameRef(), pszWKT) )
        else:
            if poLayer.GetSpatialRef() is None:
                pszWKT = "(unknown)"
            else:
                pszWKT = poLayer.GetSpatialRef().ExportToPrettyWkt()
            print( "Layer SRS WKT:\n%s" % pszWKT )

        if len(poLayer.GetFIDColumn()) > 0:
            print( "FID Column = %s" % poLayer.GetFIDColumn() )

        if nGeomFieldCount > 1:
            for iGeom in range(nGeomFieldCount):
                poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                print( "Geometry Column %d = %s" % (iGeom + 1, poGFldDefn.GetNameRef() ))
        else:
            if len(poLayer.GetGeometryColumn()) > 0:
                print( "Geometry Column = %s" % poLayer.GetGeometryColumn() )

        for iAttr in range(poDefn.GetFieldCount()):
            poField = poDefn.GetFieldDefn( iAttr )

            print( "%s: %s (%d.%d)" % ( \
                    poField.GetNameRef(), \
                    poField.GetFieldTypeName( poField.GetType() ), \
                    poField.GetWidth(), \
                    poField.GetPrecision() ))

# --------------------------------------------------------------------
#      Read, and dump features.
# --------------------------------------------------------------------
    poFeature = None

    if nFetchFID == ogr.NullFID and not bSummaryOnly:

        poFeature = poLayer.GetNextFeature()
        while poFeature is not None:
            DumpReadableFeature(poFeature, options)
            poFeature = poLayer.GetNextFeature()

    elif nFetchFID != ogr.NullFID:

        poFeature = poLayer.GetFeature( nFetchFID )
        if poFeature is None:
            print( "Unable to locate feature id %d on this layer." % nFetchFID )

        else:
            DumpReadableFeature(poFeature, options)

    return


def DumpReadableFeature( poFeature, options = None ):

    poDefn = poFeature.GetDefnRef()
    print("OGRFeature(%s):%ld" % (poDefn.GetName(), poFeature.GetFID() ))

    if 'DISPLAY_FIELDS' not in options or string_equal(options['DISPLAY_FIELDS'], 'yes'):
        for iField in range(poDefn.GetFieldCount()):

            poFDefn = poDefn.GetFieldDefn(iField)

            line =  "  %s (%s) = " % ( \
                    poFDefn.GetNameRef(), \
                    ogr.GetFieldTypeName(poFDefn.GetType()) )

            if poFeature.IsFieldSet( iField ):
                try:
                    line = line + "%s" % (poFeature.GetFieldAsString( iField ) )
                except:
                    # For Python3 on non-UTF8 strings
                    line = line + "%s" % (poFeature.GetFieldAsBinary( iField ) )
            else:
                line = line + "(null)"

            print(line)


    if poFeature.GetStyleString() is not None:

        if 'DISPLAY_STYLE' not in options or string_equal(options['DISPLAY_STYLE'], 'yes'):
            print("  Style = %s" % poFeature.GetStyleString() )

    nGeomFieldCount = poFeature.GetGeomFieldCount()
    if nGeomFieldCount > 0:
        if 'DISPLAY_GEOMETRY' not in options or not string_equal(options['DISPLAY_GEOMETRY'], 'no'):
            for iField in range(nGeomFieldCount):
                poGFldDefn = poFeature.GetDefnRef().GetGeomFieldDefn(iField)
                poGeometry = poFeature.GetGeomFieldRef(iField)
                if poGeometry is not None:
                    sys.stdout.write("  ")
                    if len(poGFldDefn.GetNameRef()) > 0 and nGeomFieldCount > 1:
                        sys.stdout.write("%s = " % poGFldDefn.GetNameRef() )
                    DumpReadableGeometry( poGeometry, "", options)

    print('')

    return


def DumpReadableGeometry( poGeometry, pszPrefix, options ):

    if pszPrefix == None:
        pszPrefix = ""

    if 'DISPLAY_GEOMETRY' in options and string_equal(options['DISPLAY_GEOMETRY'], 'SUMMARY'):

        line = ("%s%s : " % (pszPrefix, poGeometry.GetGeometryName() ))
        eType = poGeometry.GetGeometryType()
        if eType == ogr.wkbLineString or eType == ogr.wkbLineString25D:
            line = line + ("%d points" % poGeometry.GetPointCount())
            print(line)
        elif eType == ogr.wkbPolygon or eType == ogr.wkbPolygon25D:
            nRings = poGeometry.GetGeometryCount()
            if nRings == 0:
                line = line + "empty"
            else:
                poRing = poGeometry.GetGeometryRef(0)
                line = line + ("%d points" % poRing.GetPointCount())
                if nRings > 1:
                    line = line + (", %d inner rings (" % (nRings - 1))
                    for ir in range(0,nRings-1):
                        if ir > 0:
                            line = line + ", "
                        poRing = poGeometry.GetGeometryRef(ir+1)
                        line = line + ("%d points" % poRing.GetPointCount())
                    line = line + ")"
            print(line)

        elif eType == ogr.wkbMultiPoint or \
            eType == ogr.wkbMultiPoint25D or \
            eType == ogr.wkbMultiLineString or \
            eType == ogr.wkbMultiLineString25D or \
            eType == ogr.wkbMultiPolygon or \
            eType == ogr.wkbMultiPolygon25D or \
            eType == ogr.wkbGeometryCollection or \
            eType == ogr.wkbGeometryCollection25D:

                line = line + "%d geometries:" % poGeometry.GetGeometryCount()
                print(line)
                for ig in range(poGeometry.GetGeometryCount()):
                    subgeom = poGeometry.GetGeometryRef(ig)
                    from sys import version_info
                    if version_info >= (3,0,0):
                        exec('print("", end=" ")')
                    else:
                        exec('print "", ')
                    DumpReadableGeometry( subgeom, pszPrefix, options)
        else:
            print(line)

    elif 'DISPLAY_GEOMETRY' not in options or string_equal(options['DISPLAY_GEOMETRY'], 'yes') \
            or string_equal(options['DISPLAY_GEOMETRY'], 'WKT'):

        print("%s%s" % (pszPrefix, poGeometry.ExportToWkt() ))

    return

# if __name__ == '__main__':
#     version_num = int(gdal.VersionInfo('VERSION_NUM'))
#     if version_num < 1800: # because of ogr.GetFieldTypeName
#         print('ERROR: Python bindings of GDAL 1.8.0 or later required')
#         sys.exit(1)
#
#     sys.exit(main( sys.argv ))
