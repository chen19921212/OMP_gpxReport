
from examples import gpxpy
import math as mod_math


class geoSectionGpxSummaryCommon():
    gpxSegment = None

    def __init__(self):
        pass

    def processGpx(self):
        length_2d = self.gpxSegment.length_2d()
        length_3d = self.gpxSegment.length_3d()
        self["Length 2D"] = length_2d / 1000
        self["Length 3D"] = length_3d / 1000

        moving_time, stopped_time, moving_distance, stopped_distance, max_speed = self.gpxSegment.get_moving_data()
        self["Moving time"]=self.formatTime(moving_time)
        self["Stopped time"]=self.formatTime(stopped_time)
        self["Stopped distance"]=stopped_distance
        self["Max speed"]=max_speed

        uphill, downhill = self.gpxSegment.get_uphill_downhill()
        self["Total uphill"]=uphill
        self["Total downhill"]=downhill

        start_time, end_time = self.gpxSegment.get_time_bounds()
        self["Started"]=start_time
        self["Ended"]=end_time

        points_no = len(list(self.gpxSegment.walk(only_points=True)))
        self["Points"]=points_no

        distances = []
        previous_point = None
        for point in self.gpxSegment.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        self["Avg distance between points"]=sum(distances) / len(list(self.gpxSegment.walk()))

    def printGpxSegmentInfo(self, indentation='    '):
        print('%sLength 2D: %s' % (indentation, self["Length 2D"]))
        print('%sLength 3D: %s' % (indentation, self["Length 3D"]))

        print('%sMoving time: %s' % (indentation, self["Moving time"]))
        print('%sStopped time: %s' % (indentation, self["Stopped time"]))
#        print('%sStopped distance: %sm' % (indentation, self["Stopped distance"]))
        print('%sMax speed: %sm/s = %skm/h' % (indentation, self["Max speed"], self["Max speed"] * 60. ** 2 / 1000. if self["Max speed"] else 0))

        print('%sTotal uphill: %sm' % (indentation, self["Total uphill"]))
        print('%sTotal downhill: %sm' % (indentation, self["Total downhill"]))

        print('%sStarted: %s' % (indentation, self["Started"]))
        print('%sEnded: %s' % (indentation, self["Ended"]))

        print('%sAvg distance between points: %sm' % (indentation, self["Avg distance between points"]))

        print('')

    def formatTime(self, time_s):
        if not time_s:
            return 'n/a'
        minutes = mod_math.floor(time_s / 60.)
        hours = mod_math.floor(minutes / 60.)

        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))


class geoSectionGpxFileSummary(geoSectionGpxSummaryCommon, dict):
    gpxPy = None

    def __init__(self, gpxFileName=None, *arg,**kw):
        geoSectionGpxSummaryCommon.__init__(self)
        super(geoSectionGpxFileSummary, self).__init__(*arg, **kw)

        try:
            gpxFile = open(gpxFileName, 'r')
            self.gpxSegment = gpxpy.parse(gpxFile)

            self.processGpx()

            for track_no, track in enumerate(self.gpxSegment.tracks):
                for segment_no, segment in enumerate(track.segments):
                    self["Segments"]=[]
                    geoSectionGpxSegmentSummary(gpxSegment=segment, parentGpxSummary=self)

        except Exception as e:
            print("Error opening or parsing {0}: {1}.".format(gpxFileName, e))

    def printGpxSegmentInfo(self, indentation='    '):
        geoSectionGpxSummaryCommon.printGpxSegmentInfo(self)

        for gpxSegmentSummary in self["Segments"]:
            gpxSegmentSummary.printGpxSegmentInfo(indentation="               ")

class geoSectionGpxSegmentSummary(geoSectionGpxSummaryCommon, dict):

    def __init__(self, gpxSegment=None, parentGpxSummary=None, *arg,**kw):
        geoSectionGpxSummaryCommon.__init__(self)
        super(geoSectionGpxSegmentSummary, self).__init__(*arg, **kw)

        self.gpxSegment = gpxSegment

        try:
            self.processGpx()
            if parentGpxSummary!=None:
                parentGpxSummary["Segments"].append(self)

        except Exception as e:
            print("Error parsing gpxSegment: {0}.".format(e))


if __name__ == "__main__":
    geoSectionGpxSummary = geoSectionGpxFileSummary(gpxFileName = '../aa.gpx')
    geoSectionGpxSummary.printGpxSegmentInfo()


# from examples import gpxpy
# from geoNamesAdapter import *
# from rtree import index
#
# class geoNamesCommon():
#     def __init__(self):
#         pass
#
# class geoNames(geoNamesCommon, list):
#     def __init__(self, geoPoints=None, geoNamesAdapter=None, *arg,**kw):
#         geoNamesCommon.__init__(self)
#         super(geoNames, self).__init__(*arg, **kw)
#
#         if(geoPoints!=None and geoNamesAdapter!=None):
#             rtreeIdx = index.Index()
#             for i, geoName in enumerate(geoNamesAdapter):
#                 print("{0}: {1}".format(i, geoName))
#                 rtreeIdx.insert(i, (geoName["longitude"], geoName["latitude"], geoName["longitude"], geoName["latitude"]), obj=geoName)
#
#             for i, geoPoint in enumerate(geoPoints):
#                 print("-{0}- {1}, {2}:".format(i, geoPoint.latitude, geoPoint.longitude))
#                 obj = list(rtreeIdx.nearest((geoPoint.longitude, geoPoint.latitude, geoPoint.longitude, geoPoint.latitude), objects=True))[0].object
#                 if obj not in self:
#                     self.append(obj)
#
# if __name__ == "__main__":
#
#     _geoNamesAdapterCsvFile_geoNames = geoNamesAdapterCsvFile_geoNames("./PL.txt")
#     _geoNamesAdapterCsvFile_geoPortal = geoNamesAdapterCsvFile_geoPortal("./obiekty_fizjograficzne.csv")
#
#     gpx_file = open('../aa.gpx', 'r')
#     gpx = gpxpy.parse(gpx_file)
#     points = gpx.tracks[0].segments[0].points
#
#     geoNamesGpx = geoNames(points, _geoNamesAdapterCsvFile_geoNames)
#     for i, geoNameGpx in enumerate(geoNamesGpx):
#         print(geoNameGpx)
