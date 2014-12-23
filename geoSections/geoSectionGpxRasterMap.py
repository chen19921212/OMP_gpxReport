import os

from geoSections import geoSection
import matplotlib.pyplot as plt

class geoSectionGpxRasterMapCommon():
    gpxData = None
    targetDir = ""

    mplFigure = None

    def __init__(self, gpxData = None, targetDir = ""):
        self.gpxData = gpxData
        self.targetDir = targetDir

        self.mplFigure = plt.figure()
        ax = self.mplFigure.add_subplot(1,1,1)
        geoSectionViewerMap = geoSection.GeoSectionViewerMap(ax, gpxData)

        self.mplFigure.set_figheight(geoSectionViewerMap.rawMapImage.size[0]/50)
        self.mplFigure.set_figwidth(geoSectionViewerMap.rawMapImage.size[1]/50)

        geoSectionViewerMap.rawMapImage.save("geotiler.png")

class geoSectionGpxRasterMap(geoSectionGpxRasterMapCommon):
    targetFileNamePath = ""

    def __init__(self, gpxFile = "", targetDir = ""):
        gpxData = geoSection.GeoSectionGpxPoints(gpxFile)

        geoSectionGpxRasterMapCommon.__init__(self, gpxData, targetDir)

        path, filename = os.path.split(gpxFile)
        filename = os.path.splitext(filename)[0]
        targetFileName = "{0}_Map.png".format(filename)
        self.targetFileNamePath = os.path.join(self.targetDir, targetFileName)

        self.mplFigure.savefig(self.targetFileNamePath, bbox_inches='tight')

    def __str__(self):
        return self.targetFileNamePath

if __name__ == "__main__":
    geoSectionGpxRasterMap = geoSectionGpxRasterMap("aa.gpx", ".")
    pass