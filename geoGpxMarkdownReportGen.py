import os

import geoBackEnd.geoBackEnd as geoBEnd
import geoSections.geoSectionGpxSummary as geoSGpxSummary
import geoSections.geoSectionGpxRasterMap as geoSGpxRasterMap
import geoNames.geoNames as geoPoints
import geoNames.geoNamesAdapter as geoPointsSet

import gpxpy

class geoGpxMarkdownReportGenCommon():
    def __init__(self):
        pass

class geoGpxMarkdownReportGen(geoGpxMarkdownReportGenCommon):
    gpxInputFileName = "2014_11_17_Bieszczady.gpx"
    targetReportDir = "/home/ziemek/Projects/pooleTestProj/input/"
    targetReportResSubDir = "Res"

    def __init__(self):
        geoGpxMarkdownReportGenCommon.__init__(self)
#--gpx file
        gpx_file = open(self.gpxInputFileName, "r")
        gpx = gpxpy.parse(gpx_file)
        points = gpx.tracks[0].segments[0].points
#--gpx names
        geoPointsSetGeoNames = geoPointsSet.geoNamesAdapterCsvFile_geoNames("./geoNames/PL.txt")
        geoPointsSetGeoPortal = geoPointsSet.geoNamesAdapterCsvFile_geoPortal("./geoNames/obiekty_fizjograficzne.csv")

        geoNamesGpx = geoPoints.geoNames(points, geoPointsSetGeoNames)
        for i, geoNameGpx in enumerate(geoNamesGpx):
            print(geoNameGpx)

        print(geoNamesGpx)

        print(geoNamesGpx.startPoint)
        print(geoNamesGpx.endPoint)
#--gpx summary
        geoS_GpxSummary = geoSGpxSummary.geoSectionGpxFileSummary(gpxFileName = self.gpxInputFileName)
        print(geoS_GpxSummary)
#--gpx raster map
        geoS_RasterMap = geoSGpxRasterMap.geoSectionGpxRasterMap(gpxFile = self.gpxInputFileName, targetDir = self.targetReportDir, targetResDir = self.targetReportResSubDir, geoMarkers = geoNamesGpx)
        print(geoS_RasterMap)
#--gpx report backend
        #"StartPoint", "EndPoint", "StartDate", "EndDate", "GeoPoints", "Stat",

        path, filename = os.path.split(self.gpxInputFileName)
        filename = os.path.splitext(filename)[0]
        targetFileName = "{0}.md".format(filename)
        targetFileNamePath = os.path.join(self.targetReportDir, targetFileName)

        geoB_StrTemplToMd = geoBEnd.geoBackEndStrTemplToMd(templFileName='gpxReport.tpl', outputFileName=targetFileNamePath, Title = "Bieszczady", GpxFile = "Res/bieszczady.gpx", Stat = geoS_GpxSummary, StartPoint=geoNamesGpx.startPoint, EndPoint=geoNamesGpx.endPoint, StartDate=geoS_GpxSummary["Started"], EndDate=geoS_GpxSummary["Ended"], NameKeys=geoNamesGpx, RasterMap=geoS_RasterMap)

if __name__ == "__main__":
    geoGpxMarkdownReportGen = geoGpxMarkdownReportGen()

