import sys
from osgeo import gdal
from osgeo import osr

# **********************************************************************
#                               Usage()
# **********************************************************************


def Usage():
    print("Usage: gdalinfo [--help-general] [-mm] [-stats] [-hist] [-nogcp] [-nomd]\n" +
          "                [-norat] [-noct] [-nofl] [-checksum] [-mdd domain]* datasetname")
    return 1


def string_equal(a, b):
    return a.lower() == b.lower()


def get_info(filename, full_report=True):  #,  argv=None):

    bComputeMinMax = False
    bShowGCPs = True
    bShowMetadata = True
    bShowRAT = True
    bStats = False
    bApproxStats = True
    bShowColorTable = True
    bComputeChecksum = False
    bReportHistograms = False
    pszFilename = None
    papszExtraMDDomains = []
    projection = None
    hTransform = None
    bShowFileList = True

    info = {}

    # Must process GDAL_SKIP before GDALAllRegister(), but we can't call
    # GDALGeneralCmdLineProcessor before it needs the drivers to be registered
    # for the --format or --formats options
    # for( i = 1; i < argc; i++ )
    # {
    #    if EQUAL(argv[i],"--config") and i + 2 < argc and EQUAL(argv[i + 1], "GDAL_SKIP"):
    #    {
    #        CPLSetConfigOption( argv[i+1], argv[i+2] );
    #
    #        i += 2;
    #    }
    # }
    #
    # GDALAllRegister();

    # if argv is None:
    #     # argv = sys.argv
    #     argv = [filename]
    #
    #
    # argv = gdal.GeneralCmdLineProcessor(argv)
    #
    # if argv is None:
    #     return 1
    #
    # nArgc = len(argv)
# --------------------------------------------------------------------
#      Parse arguments.
# # --------------------------------------------------------------------
#     i = 1
#     while i < nArgc:
#
#         if string_equal(argv[i], "--utility_version"):
#             print("%s is running against GDAL %s" %
#                   (argv[0], gdal.VersionInfo("RELEASE_NAME")))
#             return 0
#     info["GdalVersionInfo"]
#         elif string_equal(argv[i], "-mm"):
#             bComputeMinMax = True
#         elif string_equal(argv[i], "-hist"):
#             bReportHistograms = True
#         elif string_equal(argv[i], "-stats"):
#             bStats = True
#             bApproxStats = False
#         elif string_equal(argv[i], "-approx_stats"):
#             bStats = True
#             bApproxStats = True
#         elif string_equal(argv[i], "-checksum"):
#             bComputeChecksum = True
#         elif string_equal(argv[i], "-nogcp"):
#             bShowGCPs = False
#         elif string_equal(argv[i], "-nomd"):
#             bShowMetadata = False
#         elif string_equal(argv[i], "-norat"):
#             bShowRAT = False
#         elif string_equal(argv[i], "-noct"):
#             bShowColorTable = False
#         elif string_equal(argv[i], "-mdd") and i < nArgc - 1:
#             i = i + 1
#             papszExtraMDDomains.append(argv[i])
#         elif string_equal(argv[i], "-nofl"):
#             bShowFileList = False
#         elif argv[i][0] == '-':
#             return Usage()
#         elif pszFilename is None:
#             pszFilename = argv[i]
#         else:
#             return Usage()
#
#         i = i + 1
#
#     if pszFilename is None:
#         return Usage()

    # Open dataset

    dataset = gdal.Open(filename, gdal.GA_ReadOnly)

    if dataset is None:
        info["Error"] = f"gdalinfo failed - unable to open '{filename}'"
        return info

    # general info

    driver = dataset.GetDriver()
    info["Driver"] = f"{driver.ShortName} : {driver.LongName}"

    file_list = dataset.GetFileList()
    info["Files"] = "none associated" if not file_list else file_list
    #     print("Files: none associated")
    # else:
    #     print("Files: %s" % file_list[0])
    # if bShowFileList:
    #     for i in range(1, len(file_list)):
    #         print("       %s" % file_list[i])
    info["Size X"] = dataset.RasterXSize
    info["Size Y"] = dataset.RasterYSize

    # projection

    projection = dataset.GetProjectionRef()
    if projection is not None:
        srs = osr.SpatialReference()
        if srs.ImportFromWkt(projection) == gdal.CE_None:
            projection = srs.ExportToPrettyWkt(False)

            info["SRS"] = projection
        #     print("Coordinate System is:\n%s" % pretty_wkt)
        # else:
        #     print("Coordinate System is `%s'" % projection)

    # geotransform

    geo_transform = dataset.GetGeoTransform(can_return_null=True)
    gt = {}
    if geo_transform is not None:
        if geo_transform[2] == 0.0 and geo_transform[4] == 0.0:
            gt["Origin"] = f"{geo_transform[0]:.15f}, {geo_transform[3]:.15f}"
            # print("Origin = (%.15f,%.15f)" % (
            #     geo_transform[0], geo_transform[3]))

            gt["Pixel Size"] = f"{geo_transform[1]:.15f}, {geo_transform[5]:.15f}"
            # print("Pixel Size = (%.15f,%.15f)" % (
            #     geo_transform[1], geo_transform[5]))

        else:
            gt["transform"] = f"{geo_transform[0]:.16g}, {geo_transform[1]:.16g}, {geo_transform[2]:.16g}, {geo_transform[3]:.16g}, {geo_transform[4]:.16g}, {geo_transform[5]:.16g}"
            # print("GeoTransform =\n"
            #       "  %.16g, %.16g, %.16g\n"
            #       "  %.16g, %.16g, %.16g" % (
            #           geo_transform[0],
            #           geo_transform[1],
            #           geo_transform[2],
            #           geo_transform[3],
            #           geo_transform[4],
            #           geo_transform[5]))

    info["geotransform"] = gt

    # GCPs
    gcps = {}
    if bShowGCPs and dataset.GetGCPCount() > 0:

        projection = dataset.GetGCPProjection()
        if projection is not None:

            srs = osr.SpatialReference()
            if srs.ImportFromWkt(projection) == gdal.CE_None:
                projection = srs.ExportToPrettyWkt(False)
            #     print("GCP Projection = \n%s" % pretty_wkt)
            #
            # else:
            #     print("GCP Projection = %s" %
            #           projection)
        gcps["projection"] = projection

    return str(info)
        # TODO

        # gcs = dataset.GetGCPs()
        # i = 0
        # for gcp in gcs:
        #     gcs[i] = f"{},{},{},{},{},{},{},{}"
        #
        #     print("GCP[%3d]: Id=%s, Info=%s\n"
        #           "          (%.15g,%.15g) -> (%.15g,%.15g,%.15g)" % (
        #               i, gcp.Id, gcp.Info,
        #               gcp.GCPPixel, gcp.GCPLine,
        #               gcp.GCPX, gcp.GCPY, gcp.GCPZ))
        #     i = i + 1

    info["GCPs"] =gcps

# --------------------------------------------------------------------
#      Report metadata.
# --------------------------------------------------------------------
    if bShowMetadata:
        papszMetadata = dataset.GetMetadata_List()
    else:
        papszMetadata = None
    if bShowMetadata and papszMetadata:
        print("Metadata:")
        for metadata in papszMetadata:
            print("  %s" % metadata)

    if bShowMetadata:
        for extra_domain in papszExtraMDDomains:
            papszMetadata = dataset.GetMetadata_List(extra_domain)
            if papszMetadata:
                print("Metadata (%s):" % extra_domain)
                for metadata in papszMetadata:
                    print("  %s" % metadata)

# --------------------------------------------------------------------
#      Report "IMAGE_STRUCTURE" metadata.
# --------------------------------------------------------------------
    if bShowMetadata:
        papszMetadata = dataset.GetMetadata_List("IMAGE_STRUCTURE")
    else:
        papszMetadata = None
    if bShowMetadata and papszMetadata:
        print("Image Structure Metadata:")
        for metadata in papszMetadata:
            print("  %s" % metadata)

# --------------------------------------------------------------------
#      Report subdatasets.
# --------------------------------------------------------------------
    papszMetadata = dataset.GetMetadata_List("SUBDATASETS")
    if papszMetadata:
        print("Subdatasets:")
        for metadata in papszMetadata:
            print("  %s" % metadata)

# --------------------------------------------------------------------
#      Report geolocation.
# --------------------------------------------------------------------
    if bShowMetadata:
        papszMetadata = dataset.GetMetadata_List("GEOLOCATION")
    else:
        papszMetadata = None
    if bShowMetadata and papszMetadata:
        print("Geolocation:")
        for metadata in papszMetadata:
            print("  %s" % metadata)

# --------------------------------------------------------------------
#      Report RPCs
# --------------------------------------------------------------------
    if bShowMetadata:
        papszMetadata = dataset.GetMetadata_List("RPC")
    else:
        papszMetadata = None
    if bShowMetadata and papszMetadata:
        print("RPC Metadata:")
        for metadata in papszMetadata:
            print("  %s" % metadata)

# --------------------------------------------------------------------
#      Setup projected to lat/long transform if appropriate.
# --------------------------------------------------------------------
    if projection:
        hProj = osr.SpatialReference(projection)
        if hProj is not None:
            hLatLong = hProj.CloneGeogCS()

        if hLatLong is not None:
            gdal.PushErrorHandler('CPLQuietErrorHandler')
            hTransform = osr.CoordinateTransformation(hProj, hLatLong)
            gdal.PopErrorHandler()
            if gdal.GetLastErrorMsg().find('Unable to load PROJ.4 library') != -1:
                hTransform = None

# --------------------------------------------------------------------
#      Report corners.
# --------------------------------------------------------------------
    print("Corner Coordinates:")
    GDALInfoReportCorner(dataset, hTransform, "Upper Left",
                         0.0, 0.0)
    GDALInfoReportCorner(dataset, hTransform, "Lower Left",
                         0.0, dataset.RasterYSize)
    GDALInfoReportCorner(dataset, hTransform, "Upper Right",
                         dataset.RasterXSize, 0.0)
    GDALInfoReportCorner(dataset, hTransform, "Lower Right",
                         dataset.RasterXSize,
                         dataset.RasterYSize)
    GDALInfoReportCorner(dataset, hTransform, "Center",
                         dataset.RasterXSize / 2.0,
                         dataset.RasterYSize / 2.0)

# ====================================================================
#      Loop over bands.
# ====================================================================
    for iBand in range(dataset.RasterCount):

        hBand = dataset.GetRasterBand(iBand + 1)

        # if( bSample )
        # {
        #    float afSample[10000];
        #    int   nCount;
        #
        #    nCount = GDALGetRandomRasterSample( hBand, 10000, afSample );
        #    print( "Got %d samples.\n", nCount );
        # }

        (nBlockXSize, nBlockYSize) = hBand.GetBlockSize()
        print("Band %d Block=%dx%d Type=%s, ColorInterp=%s" % (iBand + 1,
                                                               nBlockXSize, nBlockYSize,
                                                               gdal.GetDataTypeName(hBand.DataType),
                                                               gdal.GetColorInterpretationName(
                                                                   hBand.GetRasterColorInterpretation())))

        if hBand.GetDescription() is not None \
                and hBand.GetDescription():
            print("  Description = %s" % hBand.GetDescription())

        dfMin = hBand.GetMinimum()
        dfMax = hBand.GetMaximum()
        if dfMin is not None or dfMax is not None or bComputeMinMax:

            line = "  "
            if dfMin is not None:
                line = line + ("Min=%.3f " % dfMin)
            if dfMax is not None:
                line = line + ("Max=%.3f " % dfMax)

            if bComputeMinMax:
                gdal.ErrorReset()
                adfCMinMax = hBand.ComputeRasterMinMax(False)
                if gdal.GetLastErrorType() == gdal.CE_None:
                    line = line + ("  Computed Min/Max=%.3f,%.3f" % (
                        adfCMinMax[0], adfCMinMax[1]))

            print(line)

        stats = hBand.GetStatistics(bApproxStats, bStats)
        # Dirty hack to recognize if stats are valid. If invalid, the returned
        # stddev is negative
        if stats[3] >= 0.0:
            print("  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (
                stats[0], stats[1], stats[2], stats[3]))

        if bReportHistograms:

            hist = hBand.GetDefaultHistogram(force=True, callback=gdal.TermProgress)
            if hist is not None:
                dfMin = hist[0]
                dfMax = hist[1]
                nBucketCount = hist[2]
                panHistogram = hist[3]

                print("  %d buckets from %g to %g:" % (
                    nBucketCount, dfMin, dfMax))
                line = '  '
                for bucket in panHistogram:
                    line = line + ("%d " % bucket)

                print(line)

        if bComputeChecksum:
            print("  Checksum=%d" % hBand.Checksum())

        dfNoData = hBand.GetNoDataValue()
        if dfNoData is not None:
            if dfNoData != dfNoData:
                print("  NoData Value=nan")
            else:
                print("  NoData Value=%.18g" % dfNoData)

        if hBand.GetOverviewCount() > 0:

            line = "  Overviews: "
            for iOverview in range(hBand.GetOverviewCount()):

                if iOverview != 0:
                    line = line + ", "

                hOverview = hBand.GetOverview(iOverview)
                if hOverview is not None:

                    line = line + ("%dx%d" % (hOverview.XSize, hOverview.YSize))

                    pszResampling = \
                        hOverview.GetMetadataItem("RESAMPLING", "")

                    if pszResampling is not None \
                       and len(pszResampling) >= 12 \
                       and string_equal(pszResampling[0:12], "AVERAGE_BIT2"):
                        line = line + "*"

                else:
                    line = line + "(null)"

            print(line)

            if bComputeChecksum:

                line = "  Overviews checksum: "
                for iOverview in range(hBand.GetOverviewCount()):

                    if iOverview != 0:
                        line = line + ", "

                    hOverview = hBand.GetOverview(iOverview)
                    if hOverview is not None:
                        line = line + ("%d" % hOverview.Checksum())
                    else:
                        line = line + "(null)"
                print(line)

        if hBand.HasArbitraryOverviews():
            print("  Overviews: arbitrary")

        nMaskFlags = hBand.GetMaskFlags()
        if (nMaskFlags & (gdal.GMF_NODATA | gdal.GMF_ALL_VALID)) == 0:

            hMaskBand = hBand.GetMaskBand()

            line = "  Mask Flags: "
            if (nMaskFlags & gdal.GMF_PER_DATASET) != 0:
                line = line + "PER_DATASET "
            if (nMaskFlags & gdal.GMF_ALPHA) != 0:
                line = line + "ALPHA "
            if (nMaskFlags & gdal.GMF_NODATA) != 0:
                line = line + "NODATA "
            if (nMaskFlags & gdal.GMF_ALL_VALID) != 0:
                line = line + "ALL_VALID "
            print(line)

            if hMaskBand is not None and \
                    hMaskBand.GetOverviewCount() > 0:

                line = "  Overviews of mask band: "
                for iOverview in range(hMaskBand.GetOverviewCount()):

                    if iOverview != 0:
                        line = line + ", "

                    hOverview = hMaskBand.GetOverview(iOverview)
                    if hOverview is not None:
                        line = line + ("%d" % hOverview.Checksum())
                    else:
                        line = line + "(null)"

        if hBand.GetUnitType():
            print("  Unit Type: %s" % hBand.GetUnitType())

        papszCategories = hBand.GetRasterCategoryNames()
        if papszCategories is not None:

            print("  Categories:")
            i = 0
            for category in papszCategories:
                print("    %3d: %s" % (i, category))
                i = i + 1

        scale = hBand.GetScale()
        if not scale:
            scale = 1.0
        offset = hBand.GetOffset()
        if not offset:
            offset = 0.0
        if scale != 1.0 or offset != 0.0:
            print("  Offset: %.15g,   Scale:%.15g" %
                  (offset, scale))

        if bShowMetadata:
            papszMetadata = hBand.GetMetadata_List()
        else:
            papszMetadata = None
        if bShowMetadata and papszMetadata:
            print("  Metadata:")
            for metadata in papszMetadata:
                print("    %s" % metadata)

        if bShowMetadata:
            papszMetadata = hBand.GetMetadata_List("IMAGE_STRUCTURE")
        else:
            papszMetadata = None
        if bShowMetadata and papszMetadata:
            print("  Image Structure Metadata:")
            for metadata in papszMetadata:
                print("    %s" % metadata)

        hTable = hBand.GetRasterColorTable()
        if hBand.GetRasterColorInterpretation() == gdal.GCI_PaletteIndex  \
                and hTable is not None:

            print("  Color Table (%s with %d entries)" % (
                gdal.GetPaletteInterpretationName(
                    hTable.GetPaletteInterpretation()),
                hTable.GetCount()))

            if bShowColorTable:

                for i in range(hTable.GetCount()):
                    sEntry = hTable.GetColorEntry(i)
                    print("  %3d: %d,%d,%d,%d" % (
                        i,
                        sEntry[0],
                        sEntry[1],
                        sEntry[2],
                        sEntry[3]))

        if bShowRAT:
            pass
            # hRAT = hBand.GetDefaultRAT()

            # GDALRATDumpReadable( hRAT, None );

    return 0

# **********************************************************************
#                        GDALInfoReportCorner()
# **********************************************************************


def GDALInfoReportCorner(hDataset, hTransform, corner_name, x, y):

    line = "%-11s " % corner_name

# --------------------------------------------------------------------
#      Transform the point into georeferenced coordinates.
# --------------------------------------------------------------------
    adfGeoTransform = hDataset.GetGeoTransform(can_return_null=True)
    if adfGeoTransform is not None:
        dfGeoX = adfGeoTransform[0] + adfGeoTransform[1] * x \
            + adfGeoTransform[2] * y
        dfGeoY = adfGeoTransform[3] + adfGeoTransform[4] * x \
            + adfGeoTransform[5] * y

    else:
        line = line + ("(%7.1f,%7.1f)" % (x, y))
        print(line)
        return False

# --------------------------------------------------------------------
#      Report the georeferenced coordinates.
# --------------------------------------------------------------------
    if abs(dfGeoX) < 181 and abs(dfGeoY) < 91:
        line = line + ("(%12.7f,%12.7f) " % (dfGeoX, dfGeoY))

    else:
        line = line + ("(%12.3f,%12.3f) " % (dfGeoX, dfGeoY))

# --------------------------------------------------------------------
#      Transform to latlong and report.
# --------------------------------------------------------------------
    if hTransform is not None:
        pnt = hTransform.TransformPoint(dfGeoX, dfGeoY, 0)
        if pnt is not None:
            line = line + ("(%s," % gdal.DecToDMS(pnt[0], "Long", 2))
            line = line + ("%s)" % gdal.DecToDMS(pnt[1], "Lat", 2))

    print(line)

    return True


def add_info(df, file_column='fullpath'):
    df["info"] = df[file_column].apply(get_info)
    return


# if __name__ == '__main__':
#     version_num = int(gdal.VersionInfo('VERSION_NUM'))
#     if version_num < 1800:  # because of GetGeoTransform(can_return_null)
#         print('ERROR: Python bindings of GDAL 1.8.0 or later required')
#         sys.exit(1)
#
# #     sys.exit(main(sys.argv))
#     exit
