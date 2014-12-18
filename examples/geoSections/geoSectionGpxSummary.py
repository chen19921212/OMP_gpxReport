
from examples import gpxpy
import math as mod_math


class geoSectionGpxSummaryCommon(dict):
    gpxSegment = None
    indentation = "  "

    def __init__(self, *arg,**kw):
        super(geoSectionGpxSummaryCommon, self).__init__(*arg, **kw)
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

    def __str__(self):
        string = ""

        string += "{0}{1:<20s}{2}{3:.2f} km\n\r".format(self.indentation, "Length 2D:", "", self["Length 2D"])
        string += "{0}{1:<20s}{2}{3:.2f} km\n\r".format(self.indentation, "Length 3D:", "", self["Length 3D"])

        string += "{0}{1:<20s}{2}{3}\n\r".format(self.indentation, "Moving time:", "", self["Moving time"])
        string += "{0}{1:<20s}{2}{3}\n\r".format(self.indentation, "Stopped time:", "", self["Stopped time"])
        string += "{0}{1:<20s}{2}{3:.2f} m/s = {4:.2f} km/h\n\r".format(self.indentation, "Max speed:", "", self["Max speed"], self["Max speed"] * 60. ** 2 / 1000. if self["Max speed"] else 0)

        string += "{0}{1:<20s}{2}{3:.0f} m\n\r".format(self.indentation, "Total uphill:", "", self["Total uphill"])
        string += "{0}{1:<20s}{2}{3:.0f} m\n\r".format(self.indentation, "Total downhill:", "", self["Total downhill"])

        string += "{0}{1:<20s}{2}{3}\n\r".format(self.indentation, "Started:", "", self["Started"])
        string += "{0}{1:<20s}{2}{3}\n\r".format(self.indentation, "Ended:", "", self["Ended"])

#        string += "{0}{1:<20s}{2}{3:.2f} m\n\r".format(self.indentation, "Avg distance between points:", "", self["Avg distance between points"])

        return string

    def formatTime(self, time_s):
        if not time_s:
            return 'n/a'
        minutes = mod_math.floor(time_s / 60.)
        hours = mod_math.floor(minutes / 60.)

        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))

class geoSectionGpxSegmentSummary(geoSectionGpxSummaryCommon):

    def __init__(self, gpxSegment, parentGpxSummary, *arg, **kw):
        geoSectionGpxSummaryCommon.__init__(self, *arg, **kw)

        self.gpxSegment = gpxSegment

        try:
            self.processGpx()
            if parentGpxSummary!=None:
                parentGpxSummary["Segments"].append(self)

        except Exception as e:
            print("Error parsing gpxSegment: {0}.".format(e))

class geoSectionGpxDataSummary(geoSectionGpxSummaryCommon):

    def __init__(self, gpxData, *arg, **kw):
#        super(geoSectionGpxDataSummary, self).__init__(*arg, **kw)

        try:
            self.gpxSegment = gpxData

            self.processGpx()

            for track_no, track in enumerate(self.gpxSegment.tracks):
                for segment_no, segment in enumerate(track.segments):
                    self["Segments"]=[]
                    geoSectionGpxSegmentSummary(gpxSegment=segment, parentGpxSummary=self)

        except Exception as e:
            print("Error opening or parsing: {0}.".format(e))

    def __str__(self):
        str = ""

        str += geoSectionGpxSummaryCommon.__str__(self)

        for gpxSegmentSummary in self["Segments"]:
            gpxSegmentSummary.indentation = gpxSegmentSummary.indentation + gpxSegmentSummary.indentation
            str += "\n\r"
            str += gpxSegmentSummary.__str__()

        return str

class geoSectionGpxFileSummary(geoSectionGpxDataSummary):
    gpxPy = None

    def __init__(self, gpxFileName=None):
        try:
            gpxFile = open(gpxFileName, 'r')
            geoSectionGpxDataSummary.__init__(self, gpxpy.parse(gpxFile))
        except Exception as e:
            print("Error opening or parsing {0}: {1}.".format(gpxFileName, e))

if __name__ == "__main__":
    geoSectionGpxSummary = geoSectionGpxFileSummary(gpxFileName = '../aa.gpx')
    print(geoSectionGpxSummary)
