import os

from geoSections import geoSectionGpxRasterObject
from geoSections import geoSection
import matplotlib.pyplot as plt


class geoSectionGpxRasterMapCommon(geoSectionGpxRasterObject.geoSectionGpxRasterObject):
    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        geoSectionGpxRasterObject.geoSectionGpxRasterObject.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)

        geoSectionViewerMap = geoSection.GeoSectionViewerMap(self.mlpAx, gpxData, geoMarkers)

        self.mplFigure.set_figheight(geoSectionViewerMap.rawMapImage.size[0] / 50)
        self.mplFigure.set_figwidth(geoSectionViewerMap.rawMapImage.size[1] / 50)


class geoSectionGpxRasterMap(geoSectionGpxRasterMapCommon):
    targetFileNamePath = ""

    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        geoSectionGpxRasterMapCommon.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)

        #TODO: Generate unique name.
        filename = "geoSectionGpxRasterObject"
        self.targetFileName = "{0}_Map.png".format(filename)
        self.targetFileNamePath = os.path.join(self.targetDir, os.path.join(self.targetResDir, self.targetFileName))

        self.mplFigure.savefig(self.targetFileNamePath, bbox_inches='tight')

    def __str__(self):
        return os.path.join(self.targetResDir, self.targetFileName)


if __name__ == "__main__":
    geoSectionGpxRasterObject.geoSectionGpxRasterObject(None, targetDir=".", targetResDir=".", geoMarkers=None)
    geoSectionGpxRasterMapCommon(None, targetDir=".", targetResDir=".", geoMarkers=None)
    geoSectionGpxRasterMap(None, targetDir=".", targetResDir=".", geoMarkers=None)
    pass
