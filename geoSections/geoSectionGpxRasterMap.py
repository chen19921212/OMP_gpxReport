import os

from geoSections import geoSection
import matplotlib.pyplot as plt

class geoSectionGpxRasterMapCommon():
    gpxData = None
    targetDir = ""
    targetResDir = ""
    targetFileName = ""

    mplFigure = None

    def __init__(self, gpxData = None, targetDir = "", targetResDir = "", geoMarkers = None):
        self.gpxData = gpxData
        self.targetDir = targetDir
        self.targetResDir = targetResDir

        self.mplFigure = plt.figure()
        ax = self.mplFigure.add_subplot(1,1,1)
        geoSectionViewerMap = geoSection.GeoSectionViewerMap(ax, gpxData, geoMarkers)

        # self.mplFigure.set_figheight(geoSectionViewerMap.rawMapImage.size[0]/25)
        # self.mplFigure.set_figwidth(geoSectionViewerMap.rawMapImage.size[1]/25)

        self.mplFigure.set_figheight(geoSectionViewerMap.rawMapImage.size[0]/50)
        self.mplFigure.set_figwidth(geoSectionViewerMap.rawMapImage.size[1]/50)

#        geoSectionViewerMap.rawMapImage.save("geotiler.png")

class geoSectionGpxRasterMap(geoSectionGpxRasterMapCommon):
    targetFileNamePath = ""

    def __init__(self, gpxFile = "", targetDir = "", targetResDir = "", geoMarkers = None):
        gpxData = geoSection.GeoSectionGpxPoints(gpxFile)

        geoSectionGpxRasterMapCommon.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)

        path, filename = os.path.split(gpxFile)
        filename = os.path.splitext(filename)[0]
        self.targetFileName = "{0}_Map.png".format(filename)
        self.targetFileNamePath = os.path.join(self.targetDir, os.path.join(self.targetResDir, self.targetFileName))

        self.mplFigure.savefig(self.targetFileNamePath, bbox_inches='tight')

    def __str__(self):
        return os.path.join(self.targetResDir, self.targetFileName)

if __name__ == "__main__":
    geoSectionGpxRasterMap = geoSectionGpxRasterMap("aa.gpx", ".")
    pass
