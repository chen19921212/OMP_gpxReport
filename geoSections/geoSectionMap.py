from geoCommon.geoConfig import GeoConfig
from string import Template

class geoSectionMapCommon():
    def __init__(self):
        outputPath = GeoConfig.geoReport["outputPath"]
        outputResSubPath = GeoConfig.geoReport["outputResSubPath"]


class geoSectionMap(geoSectionMapCommon):
    gpxFroJsMap = None

    def __init__(self, gpxFroJsMap = None):
        geoSectionMapCommon.__init__(self)
        self.gpxFroJsMap = gpxFroJsMap

    def __str__(self):
        outStr = ""

        if(self.gpxFroJsMap != None):
            jsMapFileIn = open("geoSectionGallery_Map.tpl", 'r')

            jsMapTemplate = Template(jsMapFileIn.read())
            outStr = jsMapTemplate.substitute({"GpxFile": self.gpxFroJsMap})

        return outStr

if __name__ == "__main__":
    geoSectionMap = geoSectionMap(gpxFroJsMap = "testGpx.gpx")
    print(geoSectionMap)
