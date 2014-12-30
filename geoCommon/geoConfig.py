import os


class GeoConfigCommon():
    def __init__(self):
        pass


class GeoConfig(GeoConfigCommon):
    geoReport = {"outputPath": "/home/ziemek/Projects/pooleTestProj/input/", "outputResSubPath": "highslide/images/"}

    def __init__(self):
        GeoConfigCommon.__init__()


if __name__ == "__main__":
    geoConfig = GeoConfig()

    print(geoConfig.geoReport["outputPath"])
    print(geoConfig.geoReport["outputResSubPath"])
    print(os.path.join(geoConfig.geoReport["outputPath"], geoConfig.geoReport["outputResSubPath"]))
    print("------------------")
    print(GeoConfig.geoReport["outputPath"])
    print(GeoConfig.geoReport["outputResSubPath"])
    print(os.path.join(GeoConfig.geoReport["outputPath"], GeoConfig.geoReport["outputResSubPath"]))
