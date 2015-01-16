import os
import shutil

from geoCommon.geoConfig import GeoConfig

import geoBackEnd.geoBackEnd as geoBEnd
import geoSections.geoSectionGpxSummary as geoSGpxSummary
import geoSections.geoSectionMap as geoSMap
import geoSections.geoSectionGpxRasterMap as geoSGpxRasterMap
import geoSections.geoSectionGpxRasterProfile as geoSGpxRasterProfile
import geoSections.geoSectionGallery as geoSGallery
import geoSections.geoSectionGpxFile as geoSGpxFile
import geoSections.geoSection as geoSection
import geoNames.geoNames as geoPoints
import geoNames.geoNamesAdapter as geoPointsSet

import gpxpy

class geoGpxMarkdownReportGenCommon():
    def __init__(self):
        pass

class geoGpxMarkdownReportGen(geoGpxMarkdownReportGenCommon):
    genInSeparateFolder = True
    reportTitle = ""
    gpxInputFileName = ""
    targetReportDir = ""
    targetReportSubDir = ""
    targetReportResSubDir = ""

    def __init__(self, gpxInputFileName, genInSeparateFolder=True, reportTitle = ""):
        geoGpxMarkdownReportGenCommon.__init__(self)

        self.genInSeparateFolder = genInSeparateFolder
        self.gpxInputFileName = gpxInputFileName
        self.targetReportDir = GeoConfig.geoReport["outputPath"]
        self.targetReportResSubDir = GeoConfig.geoReport["outputResSubPath"]

        if(reportTitle != ""):
            self.reportTitle = reportTitle
        else:
            self.reportTitle = "Report for {0}".format(self.gpxInputFileName)

        if(self.genInSeparateFolder != False):
            head, tail = os.path.split(self.gpxInputFileName)
            self.targetReportSubDir, tail = os.path.splitext(tail)
#            self.targetReportDir = os.path.join(self.targetReportDir, self.targetReportSubDir)
#            self.targetReportResSubDir = os.path.join(self.targetReportSubDir, self.targetReportResSubDir)

        print("self.targetReportDir:       {0}".format(self.targetReportDir))
        print("self.targetReportSubDir:    {0}".format(self.targetReportSubDir))
        print("self.targetReportResSubDir: {0}".format(self.targetReportResSubDir))

    def gpxFileReportGen(self, gpxFile=None):
        if (gpxFile is not None):
            if ((os.path.splitext(gpxFile)[1][1:]).lower() == "gpx"):
                print("processing: {0}".format(gpxFile))

    def gpxDataDirProcess(self, gpxDirectory=None):
        if (gpxDirectory is not None):
            for root, dirs, files in os.walk(gpxDirectory):
                for file in files:
                    self.gpxFileReportGen(file)

    def process(self):
#--pre process
        try:
            os.makedirs(os.path.join(self.targetReportDir,  self.targetReportSubDir))
        except OSError:
            pass

        try:
            os.makedirs(os.path.join(self.targetReportDir, self.targetReportSubDir, self.targetReportResSubDir))
        except OSError:
            pass

        resFullPath = os.path.join(self.targetReportDir, self.targetReportSubDir, self.targetReportResSubDir)
        shutil.copy2(self.gpxInputFileName, resFullPath)

#--gpx file
        gpxFile = open(self.gpxInputFileName, "r")
        gpx = gpxpy.parse(gpxFile)
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
#--gpx data
        gpxData = geoSection.GeoSectionGpxPoints(self.gpxInputFileName)
#--gpx map
        geoS_Map = geoSMap.geoSectionMap(gpxFroJsMap = os.path.join(self.targetReportResSubDir, self.gpxInputFileName))
        print(geoS_Map)
#--gpx summary
        geoS_GpxSummary = geoSGpxSummary.geoSectionGpxFileSummary(gpxFileName = self.gpxInputFileName)
        print(geoS_GpxSummary)
#--gpx raster map
        geoS_RasterMap = geoSGpxRasterMap.geoSectionGpxRasterMap(gpxData = gpxData, targetDir = self.targetReportDir, targetResDir = os.path.join(self.targetReportSubDir, self.targetReportResSubDir), geoMarkers = geoNamesGpx)
        print(geoS_RasterMap)
#--gpx raster profile
        geoS_RasterProfile = geoSGpxRasterProfile.geoSectionGpxRasterProfile(gpxData = gpxData, targetDir = self.targetReportDir, targetResDir = os.path.join(self.targetReportSubDir, self.targetReportResSubDir), geoMarkers = geoNamesGpx)
        print(geoS_RasterProfile )
#--gpx gallery
        geoS_Gallery = geoSGallery.geoSectionGallery(picturesRepository= "geoSections/Pic", targetDir = self.targetReportDir, targetResDir = os.path.join(self.targetReportSubDir, self.targetReportResSubDir))
        print(geoS_Gallery)
#--gpx report backend
        #"StartPoint", "EndPoint", "StartDate", "EndDate", "GeoPoints", "Stat",

        path, filename = os.path.split(self.gpxInputFileName)
        filename = os.path.splitext(filename)[0]
        targetFileName = "{0}.md".format(filename)
        targetFileNamePath = os.path.join(self.targetReportDir, self.targetReportSubDir, targetFileName)

#        geoB_StrTemplToMd = geoBEnd.geoBackEndStrTemplToMd(process=True, templFileName='gpxReport.tpl', outputFileName=targetFileNamePath, Title = "Bieszczady", GpxFile = "Res/bieszczady.gpx", Stat = geoS_GpxSummary, StartPoint=geoNamesGpx.startPoint, EndPoint=geoNamesGpx.endPoint, StartDate=geoS_GpxSummary["Started"], EndDate=geoS_GpxSummary["Ended"], NameKeys=geoNamesGpx, RasterMap=geoS_RasterMap, RasterProfile=geoS_RasterProfile)
        geoB_StrTemplToMd = geoBEnd.geoBackEndStrTemplToMd(templFileName='gpxReport.tpl', outputFileName=targetFileNamePath)
#        geoB_StrTemplToMd["process"]=True
        geoB_StrTemplToMd["templFileName"]='gpxReport.tpl'
        geoB_StrTemplToMd["outputFileName"]=targetFileNamePath
        geoB_StrTemplToMd["Title"] = self.reportTitle
        geoB_StrTemplToMd["GpxFile"] = geoS_Map
        geoB_StrTemplToMd["Stat"] = geoS_GpxSummary
        geoB_StrTemplToMd["StartPoint"]=geoNamesGpx.startPoint
        geoB_StrTemplToMd["EndPoint"]=geoNamesGpx.endPoint
        geoB_StrTemplToMd["StartDate"]=geoS_GpxSummary["Started"]
        geoB_StrTemplToMd["EndDate"]=geoS_GpxSummary["Ended"]
        geoB_StrTemplToMd["NameKeys"]=geoNamesGpx
        geoB_StrTemplToMd["RasterMap"]=geoS_RasterMap
        geoB_StrTemplToMd["RasterProfile"]=geoS_RasterProfile
        geoB_StrTemplToMd["PicGallery"]= geoS_Gallery

        geoB_StrTemplToMd.process()

if __name__ == "__main__":
    geoGpxMarkdownReportGen = geoGpxMarkdownReportGen(gpxInputFileName = "2014-11-16_06-11-59.gpx", genInSeparateFolder=True)
#    geoGpxMarkdownReportGen.process()

#    geoGpxMarkdownReportGen.gpxDataDirProcess("exampleData")

    geoSGpxFile = geoSGpxFile.geoSectionGpxFile(geoGpxMarkdownReportGen.gpxInputFileName, geoGpxMarkdownReportGen.targetReportDir, geoGpxMarkdownReportGen.targetReportSubDir, geoGpxMarkdownReportGen.targetReportResSubDir)
    print("geoSGpxFile: {0}".format(geoSGpxFile))

