
from examples import gpxpy
from geoNamesAdapter import *
from rtree import index

class geoNamesCommon(list):
    def __init__(self, *arg, **kw):
        super(geoNamesCommon, self).__init__(*arg, **kw)
        pass

class geoNames(geoNamesCommon, list):
    def __init__(self, geoPoints=None, geoNamesAdapter=None, *arg,**kw):
        geoNamesCommon.__init__(self)

        if(geoPoints!=None and geoNamesAdapter!=None):
            rtreeIdx = index.Index()
            for i, geoName in enumerate(geoNamesAdapter):
                print("{0}: {1}".format(i, geoName))
                rtreeIdx.insert(i, (geoName["longitude"], geoName["latitude"], geoName["longitude"], geoName["latitude"]), obj=geoName)

            for i, geoPoint in enumerate(geoPoints):
                print("-{0}- {1}, {2}:".format(i, geoPoint.latitude, geoPoint.longitude))
                obj = list(rtreeIdx.nearest((geoPoint.longitude, geoPoint.latitude, geoPoint.longitude, geoPoint.latitude), objects=True))[0].object
                if obj not in self:
                    self.append(obj)

    @property
    def startPoint(self):
        return self[0]["name"]

    @property
    def endPoint(self):
        return self[len(self)-1]["name"]

    def __str__(self):
        str = ""

        for i, geoNameGpx in enumerate(self):
            str += "{0}.{1}\n\r".format(i, geoNameGpx["name"])

        return str

if __name__ == "__main__":

    _geoNamesAdapterCsvFile_geoNames = geoNamesAdapterCsvFile_geoNames("./PL.txt")
    _geoNamesAdapterCsvFile_geoPortal = geoNamesAdapterCsvFile_geoPortal("./obiekty_fizjograficzne.csv")

    gpx_file = open('../aa.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)
    points = gpx.tracks[0].segments[0].points

    geoNamesGpx = geoNames(points, _geoNamesAdapterCsvFile_geoNames)
    for i, geoNameGpx in enumerate(geoNamesGpx):
        print(geoNameGpx)

    print(geoNamesGpx)

    print(geoNamesGpx.startPoint)
    print(geoNamesGpx.endPoint)
