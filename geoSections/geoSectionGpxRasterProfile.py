import os

from geoSections import geoSectionGpxRasterObject
from geoSections import geoSection


class geoSectionGpxRasterProfileCommon():
    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        geoSectionGpxRasterObject.geoSectionGpxRasterObject.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)

        geoSectionViewerMap = geoSection.GeoSectionViewerProfile(self.mlpAx, gpxData, geoMarkers)

        # self.mplFigure.set_figheight(geoSectionViewerMap.rawMapImage.size[0] / 50)
        # self.mplFigure.set_figwidth(geoSectionViewerMap.rawMapImage.size[1] / 50)

        self.mplFigure.set_figheight(10)
        self.mplFigure.set_figwidth(50)


class geoSectionGpxRasterProfile(geoSectionGpxRasterProfileCommon):
    targetFileNamePath = ""

    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        geoSectionGpxRasterProfileCommon.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)

        # TODO: Generate unique name.
        filename = "geoSectionGpxRasterObject"
        self.targetFileName = "{0}_Profile.png".format(filename)
        self.targetFileNamePath = os.path.join(self.targetDir, os.path.join(self.targetResDir, self.targetFileName))

        self.mplFigure.savefig(self.targetFileNamePath, bbox_inches='tight')

    def __str__(self):
        return os.path.join(self.targetResDir, self.targetFileName)


if __name__ == "__main__":
    geoSectionGpxRasterProfile = geoSectionGpxRasterProfile()
