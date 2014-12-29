import matplotlib.pyplot as plt


class geoSectionGpxRasterObjectCommon():
    gpxData = None
    geoMarkers = None
    targetDir = ""
    targetResDir = ""
    targetFileName = ""

    mplFigure = None
    mlpAx = None

    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        self.gpxData = gpxData
        self.targetDir = targetDir
        self.targetResDir = targetResDir
        self.geoMarkers = geoMarkers

        self.mplFigure = plt.figure()
        self.mlpAx = self.mplFigure.add_subplot(1, 1, 1)


class geoSectionGpxRasterObject(geoSectionGpxRasterObjectCommon):
    def __init__(self, gpxData=None, targetDir="", targetResDir="", geoMarkers=None):
        geoSectionGpxRasterObjectCommon.__init__(self, gpxData, targetDir, targetResDir, geoMarkers)


if __name__ == "__main__":
    geoSectionGpxRasterObject = geoSectionGpxRasterObject()
