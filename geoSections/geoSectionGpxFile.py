from string import Template

class geoSectionGpxFileCommon():
    def __init__(self):
        pass


class geoSectionGpxFile(geoSectionGpxFileCommon):
    gpxInputFileName = ""
    targetReportDir = ""
    targetReportSubDir = ""
    targetReportResSubDir = ""

    def __init__(self, gpxInputFileName, targetReportDir, targetReportSubDir, targetReportResSubDir):
        geoSectionGpxFileCommon.__init__(self)

        self.gpxInputFileName = gpxInputFileName
        self.targetReportDir = targetReportDir
        self.targetReportSubDir = targetReportSubDir
        self.targetReportResSubDir = targetReportResSubDir

    def __str__(self):
        outStr = "---------"

        jsMapFileIn = open("gpxFileReport.tpl", 'r')

        jsMapTemplate = Template(jsMapFileIn.read())
#        outStr = jsMapTemplate.substitute({"GpxFile": self.gpxFroJsMap})

        return outStr


if __name__ == "__main__":
    geoSectionGpxFile = geoSectionGpxFile()
