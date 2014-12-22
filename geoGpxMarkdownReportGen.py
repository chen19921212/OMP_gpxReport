import geoBackEnd.geoBackEnd as geoBEnd
import geoSections.geoSectionGpxSummary as geoSGpxSummary
import geoNames.geoNames as geoPoints
import geoNames.geoNamesAdapter as geoPointsSet

import gpxpy

class geoGpxMarkdownReportGenCommon():
    def __init__(self):
        pass

class geoGpxMarkdownReportGen(geoGpxMarkdownReportGenCommon):
    def __init__(self):
        geoGpxMarkdownReportGenCommon.__init__(self)
#--gpx file
        gpx_file = open('2014_11_17_Bieszczady.gpx', 'r')
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
        geoS_GpxSummary = geoSGpxSummary.geoSectionGpxFileSummary(gpxFileName = '2014_11_17_Bieszczady.gpx')
        print(geoS_GpxSummary)
#--gpx report backend
        #"StartPoint", "EndPoint", "StartDate", "EndDate", "GeoPoints", "Stat",
        geoB_StrTemplToMd = geoBEnd.geoBackEndStrTemplToMd(templFileName='gpxReport.tpl', outputFileName='/home/ziemek/Projects/pooleTestProj/input/gpxReport.md', Title = "Bieszczady", GpxFile = "Res/bieszczady.gpx", Stat = geoS_GpxSummary, StartPoint=geoNamesGpx.startPoint, EndPoint=geoNamesGpx.endPoint, StartDate=geoS_GpxSummary["Started"], EndDate=geoS_GpxSummary["Ended"], NameKeys=geoNamesGpx)

if __name__ == "__main__":
    geoGpxMarkdownReportGen = geoGpxMarkdownReportGen()

