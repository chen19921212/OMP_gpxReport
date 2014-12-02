# class geoSectionCommon():
#     def __init__(self):
#         pass
#
# class geoSection(geoSectionCommon, list):
#     # def __init__(self, geoPoints=None, geoSectionAdapter=None, *arg,**kw):
#     #     geoSectionCommon.__init__(self)
#     #     super(geoSection, self).__init__(*arg, **kw)
#     #
#     #     if(geoPoints!=None and geoSectionAdapter!=None):
#     #         rtreeIdx = index.Index()
#     #         for i, geoName in enumerate(geoSectionAdapter):
#     #             print("{0}: {1}".format(i, geoName))
#     #             rtreeIdx.insert(i, (geoName["longitude"], geoName["latitude"], geoName["longitude"], geoName["latitude"]), obj=geoName)
#     #
#     #         for i, geoPoint in enumerate(geoPoints):
#     #             print("-{0}- {1}, {2}:".format(i, geoPoint.latitude, geoPoint.longitude))
#     #             obj = list(rtreeIdx.nearest((geoPoint.longitude, geoPoint.latitude, geoPoint.longitude, geoPoint.latitude), objects=True))[0].object
#     #             if obj not in self:
#     #                 self.append(obj)
#     pass
#
# if __name__ == "__main__":
#     pass

from __future__ import print_function
from matplotlib.dates import strpdate2num
#from matplotlib.mlab import load
import numpy as np
from pylab import figure, show
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt


from examples import gpxpy

gpx_file = open('../aa.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
points = gpx.tracks[0].segments[0].points

latitudes = []
longitudes = []
elevations = []
timestamps = []

for point in points:
    latitudes.append(point.latitude)
    longitudes.append(point.longitude)
    elevations.append(point.elevation)
    timestamps.append(point.time)

#latitude, longitude, elevation time

# datafile = cbook.get_sample_data('msft.csv', asfileobj=False)
# print('loading', datafile)
#
# dates, closes = np.loadtxt(
#     datafile, delimiter=',',
#     converters={0:strpdate2num('%d-%b-%y')},
#     skiprows=1, usecols=(0,2), unpack=True)
#
#fig = figure()
fig = plt.figure()

ax = fig.add_subplot(111)
ax.plot_date(timestamps, elevations, '-')
fig.autofmt_xdate()

plt.savefig('elevation.png')
plt.show()


plt.close()

