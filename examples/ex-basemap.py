#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
# Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

"""
Matplotlib Basemap Toolkit example.
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from mpl_toolkits.basemap import Basemap

import logging

logging.basicConfig(level=logging.DEBUG)

import geotiler

import math

#---------------------------------------------
import gpxpy


def get_xy_from_points_mercator(points):
    # http://fr.wikipedia.org/wiki/Projection_de_Mercator
    longitude_origine = sum([p.longitude for p in points]) / len(points)
    coords = []
    for p in points:
        x = p.longitude - longitude_origine
        y = math.log(math.tan(math.radians(math.pi / 4 + p.latitude / 2)))
        coords.append((x, y))
    return coords


latitudeMax = 0
latitudeMin = 360
longitudeMax = 0
longitudeMin = 360

gpx_file = open('aa.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
points = gpx.tracks[0].segments[0].points

latitudes = []
longitudes = []
elevations = []

for point in points:
    latitudes.append(point.latitude)
    longitudes.append(point.longitude)
    elevations.append(point.elevation)

# latitudes  = [point.latitude  for i,point in enumerate(points)]
# longitudes = [point.longitude for i,point in enumerate(points)]
# elevations = [point.elevation for i,point in enumerate(points)]

latitudeMax = max(latitudes)
latitudeMin = min(latitudes)
longitudeMax = max(longitudes)
longitudeMin = min(longitudes)
elevationMax = max(elevations)
elevationMin = min(elevations)

scalledMax = 1
scalledMin = 30

scalledElevations = [
    ((((point.elevation - elevationMin) * (scalledMax - scalledMin)) / (elevationMax - elevationMin)) + scalledMin) for
    i, point in enumerate(points)]

#NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
#NewValue = (((point.elevation - elevationMin) * (scalledMax - scalledMin)) / (elevationMax - elevationMin)) + scalledMin

# for i,point in enumerate(points):
#     print('Point at ({0},{1},{2}) : {3}'.format(point.latitude, point.longitude, point.elevation, point.time))

# if(point.latitude > latitudeMax):
#     latitudeMax = point.latitude
# if(point.latitude < latitudeMin):
#     latitudeMin = point.latitude
# if(point.longitude > longitudeMax):
#     longitudeMax = point.longitude
# if(point.longitude < longitudeMin):
#     longitudeMin = point.longitude

# x,y = map(point.longitude, point.latitude)
# map.plot(x, y, 'bo', markersize=12)
#---------------------------------------------

#bbox = 11.78560, 46.48083, 11.79067, 46.48283
bbox = longitudeMin, latitudeMin, longitudeMax, latitudeMax

#fig = plt.figure(figsize=(30, 30))
#ax = plt.subplot(111)

#
# download background map using OpenStreetMap
#
mm = geotiler.Map(extent=bbox, zoom=14)

img = geotiler.render_map(mm)
#
# create basemap
#

fig = plt.figure(figsize=(img.size[0] / 100, img.size[1] / 100))

map = Basemap(
    llcrnrlon=bbox[0], llcrnrlat=bbox[1],
    urcrnrlon=bbox[2], urcrnrlat=bbox[3],
    projection='merc',
    resolution='i'
)

map.imshow(img, origin='upper')

# plot custom points
#
# x0, y0 = 11.78816, 46.48114 # http://www.openstreetmap.org/search?query=46.48114%2C11.78816
# x1, y1 = 11.78771, 46.48165 # http://www.openstreetmap.org/search?query=46.48165%2C11.78771
x, y = map(longitudes, latitudes)
#x, y = mm.rev_geocode(longitudes, latitudes) for p in points
#map.scatter(x, y, c='red', s=scalledElevations, marker='o', cmap=cm.hot_r, alpha=0.4)
map.scatter(longitudes, latitudes, c='red', s=scalledElevations, marker='o', cmap=cm.hot_r, alpha=0.4, latlon=True)
map.plot(x, y, 'k', c='red')

# for i,point in enumerate(points):
#     print('Point at ({0},{1},{2}) : {3}'.format(point.latitude, point.longitude, point.elevation,point.time))
#     x,y = map(point.longitude, point.latitude)
#     map.plot(x, y, 'bo', markersize=1)

#map.plot(get_xy_from_points_mercator(points), 'k', c='red')

# for i,point in enumerate(points):
#     print('Point at ({0},{1},{2}) : {3}'.format(point.latitude, point.longitude, point.elevation,point.time))
#
#     xpt,ypt = map(point.longitude, point.latitude)
#     # convert back to lat/lon
#     map.plot(xpt,ypt,'bo')  # plot a blue dot there

# plt.savefig('ex-basemap.png')
# plt.close()

#---------------------------------------------------------
# for i, point in enumerate(points):
#     results = Geocoder.reverse_geocode(point.latitude, point.longitude)
#     print("-{0}- {1}, {2}: {3}".format(i, point.latitude, point.longitude, results[0]))

# from geopy.geocoders import GeoNames
#
# from geopy.exc import (
#     GeocoderServiceError,
#     ConfigurationError,
#     GeocoderTimedOut,
#     GeocoderAuthenticationFailure,
#     GeocoderQuotaExceeded,
#     GeocoderQueryError,
#     GeocoderInsufficientPrivileges,
#     GeocoderUnavailable,
#     GeocoderParseError,
# )
#
# geolocator = GeoNames(username="syntaxErrorAtkontopl")
# for i, point in enumerate(points):
#     print("-{0}- {1}, {2}:".format(i, point.latitude, point.longitude))
#     try:
#         results = geolocator.reverse("{0},{1}".format(point.latitude, point.longitude))
#         if results != None:
#             for result in results:
#                 print("\t\t\t{0}\n\r".format(result))
#     except GeocoderTimedOut:
#         print("\t\t\tTimeout Error\n\r")
#     except:
#         print("\t\t\tOther Error\n\r")


#---------------------------------------------------------

# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int)
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format

import csv

from rtree import index
idx = index.Index()

with open("./geoNames/PL.txt", newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:

        geoObject = {}
        geoObject["geonameid"]              = int(row[0])
        geoObject["name"]                   = row[1]
        geoObject["asciiname"]              = row[2]
        geoObject["alternatenames"]         = row[3]
        geoObject["latitude"]               = float(row[4])
        geoObject["longitude"]              = float(row[5])
        geoObject["feature class"]          = row[6]
        geoObject["feature code"]           = row[7]
        geoObject["country code"]           = row[8]
        geoObject["cc2"]                    = row[9]
        geoObject["admin1 code"]            = row[10]
        geoObject["admin2 code"]            = row[11]
        geoObject["admin3 code"]            = row[12]
        geoObject["admin4 code"]            = row[13]
        geoObject["population"]             = row[14]
        geoObject["elevation"]              = row[15]
        geoObject["dem"]                    = row[16]
        geoObject["timezone"]               = row[17]
        geoObject["modification date"]      = row[18]

        print("idx: {0} lon:{1} lat:{2} name:{3}".format(geoObject["geonameid"], geoObject["longitude"], geoObject["latitude"], geoObject["name"]))
        idx.insert(int(row[0]), (geoObject["longitude"], geoObject["latitude"], geoObject["longitude"], geoObject["latitude"]), obj=geoObject)

keyObjects = []

for i, point in enumerate(points):
    print("-{0}- {1}, {2}:".format(i, point.latitude, point.longitude))
    obj = list(idx.nearest((point.longitude, point.latitude, point.longitude, point.latitude), objects=True))[0].object
    if obj not in keyObjects:
        keyObjects.append(obj)

for keyObject in keyObjects:
    print(keyObject)

    xy = map(keyObject["longitude"], keyObject["latitude"])

    plt.annotate(
        keyObject["name"],
        xy, xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.text(xy[0], xy[1], keyObject["name"],fontsize=9,
                    ha='center',va='top',color='r',
                    bbox = dict(boxstyle="round,pad=0.5",ec='None',fc=(1,1,1,0.5)))

plt.savefig('ex-basemap.png')
plt.close()

#---------------------------------------------------------

#Tarnica >>---------> 49°04'29''	22°43'35''	140815,06	772032,01

# >>> d = {'foo': 42, 'bar': 'quux'}
# >>> for k in d:
# ...   print k, d[k]
# ...
# foo 42
# bar quux

# vim: sw=4:et:ai
