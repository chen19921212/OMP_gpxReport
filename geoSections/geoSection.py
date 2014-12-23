from encodings.punycode import selective_find
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import axes3d
from matplotlib.figure import Figure

import logging
logging.basicConfig(level=logging.DEBUG)

class GeoSectionCommon():
    def __init__(self):
        pass

class GeoSection(GeoSectionCommon):
    def __init__(self):
        GeoSectionCommon.__init__(self)

# class GeoSectionException(Exception):
#     def __index__(self):
#         Exception
#--Data-----------------------------------------------------------------------------------------------------------------
from examples import gpxpy

class GeoSectionData(GeoSectionCommon):
    def __init__(self):
        GeoSectionCommon.__init__(self)

class GeoSectionDataList(GeoSectionData, list):
    def __init__(self, *arg,**kw):
        GeoSectionData.__init__(self)
        super(GeoSectionDataList, self).__init__(*arg, **kw)

class GeoSectionGpxPoints(GeoSectionDataList):
    def __init__(self):
        GeoSectionDataList.__init__(self)

    def __init__(self, gpxData=None):
        GeoSectionDataList.__init__(self)
        self.gpxData = gpxData

    def __init__(self, gpxFileName=None):
        GeoSectionDataList.__init__(self)

        gpxFile = open(gpxFileName, 'r')
        gpx = gpxpy.parse(gpxFile)
        self.extend(gpx.tracks[0].segments[0].points)

    def getLatLongElevTs(self):
        latitudes = []
        longitudes = []
        elevations = []
        timestamps = []

        for gpxPoint in self:
            latitudes.append(gpxPoint.latitude)
            longitudes.append(gpxPoint.longitude)
            elevations.append(gpxPoint.elevation)
            timestamps.append(gpxPoint.time)

        return latitudes, longitudes, elevations, timestamps

#--Viewer-----------------------------------------------------------------------------------------------------------
class GeoSectionViewer(GeoSectionCommon):
    def __init__(self):
        GeoSectionCommon.__init__(self)

class GeoSectionViewerMatplotLib(GeoSectionViewer):
    subPlot = None
    def __init__(self):
        GeoSectionViewer.__init__(self)

    def __init__(self, subPlot = None):
        GeoSectionViewer.__init__(self)
        self.subPlot = subPlot

class GeoSectionViewerGpxData(GeoSectionViewerMatplotLib):
    gpxData = None

    def __init__(self):
        GeoSectionViewerMatplotLib.__init__(self)

    def __init__(self, subplot, gpxData):
        GeoSectionViewerMatplotLib.__init__(self, subplot)
        self.gpxData = gpxData
#--Profile--
class GeoSectionViewerProfile(GeoSectionViewerGpxData):
    def __init__(self):
        GeoSectionViewerGpxData.__init__(self)

    def __init__(self, subPlot = None, gpxData = None):
        GeoSectionViewerGpxData.__init__(self, subPlot, gpxData)

        latitudes, longitudes, elevations, timestamps = self.gpxData.getLatLongElevTs()
        subPlot.fill_between(timestamps, elevations, facecolor='blue', alpha=0.5)
#--Map--
import geotiler
from mpl_toolkits.basemap import Basemap

class GeoSectionViewerMap(GeoSectionViewerGpxData):
    rawMapImage = None

    def __init__(self):
        GeoSectionViewerGpxData.__init__(self)

    def __init__(self, subPlot = None, gpxData = None):
        GeoSectionViewerGpxData.__init__(self, subPlot, gpxData)

        latitudes, longitudes, elevations, timestamps = self.gpxData.getLatLongElevTs()

        latitudeMax = max(latitudes)
        latitudeMin = min(latitudes)
        longitudeMax = max(longitudes)
        longitudeMin = min(longitudes)
        elevationMax = max(elevations)
        elevationMin = min(elevations)

        scalledMax = 30
        scalledMin = 1

        scalledElevations = [((((point.elevation - elevationMin) * (scalledMax - scalledMin)) / (elevationMax - elevationMin)) + scalledMin) for i, point in enumerate(self.gpxData)]
        bbox = longitudeMin, latitudeMin, longitudeMax, latitudeMax

        mm = geotiler.Map(extent=bbox, zoom=14)
        self.rawMapImage = geotiler.render_map(mm)

        map = Basemap(
            llcrnrlon=bbox[0], llcrnrlat=bbox[1],
            urcrnrlon=bbox[2], urcrnrlat=bbox[3],
            projection='merc',
            resolution='i',
            ax=self.subPlot)
        map.imshow(self.rawMapImage, aspect='auto', origin='upper')
        #--draw path
        map.scatter(longitudes, latitudes, c='red', s=scalledElevations, marker='o', cmap=cm.hot_r, alpha=0.4, latlon=True)
        map.plot(longitudes, latitudes, 'k', c='red', latlon=True)
        #--draw labels
        # for keyObject in keyObjects:
        #     print(keyObject)
        #
        #     xy = map(keyObject["longitude"], keyObject["latitude"])
        #
        #     plt.annotate(
        #         keyObject["name"],
        #         xy, xytext = (-20, 20),
        #         textcoords = 'offset points', ha = 'right', va = 'bottom',
        # #        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        #         bbox = dict(fc = 'yellow', alpha = 0.5),
        #         arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        #
        #     plt.text(xy[0], xy[1], keyObject["name"],fontsize=9,
        #                     ha='center',va='top',color='r',
        #                     bbox = dict(ec='None',fc=(1,1,1,0.5)))
#--3d--
class GeoSectionViewer3d(GeoSectionViewerGpxData):
    def __init__(self):
        GeoSectionViewerGpxData.__init__(self)

    def __init__(self, subPlot = None, gpxData = None):
        GeoSectionViewerGpxData.__init__(self, subPlot, gpxData)

        latitudes, longitudes, elevations, timestamps = self.gpxData.getLatLongElevTs()
        subPlot.plot(longitudes, latitudes, elevations)
#--Viewer-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    import matplotlib.pyplot    as plt
    import matplotlib.gridspec  as gridspec

    import matplotlib.image     as mpimg

    # gs = gridspec.GridSpec(3, 3)
    # ax1 = plt.subplot(gs[0, :])
    # ax2 = plt.subplot(gs[1,:-1])
    # ax3 = plt.subplot(gs[1:, -1])
    # ax4 = plt.subplot(gs[-1,0])
    # ax5 = plt.subplot(gs[-1,-2])

    # gs = gridspec.GridSpec(2, 1)
    # ax1 = plt.subplot(gs[0, 0])
    # ax2 = plt.subplot(gs[1, 0])

    # subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    #
    # left  = 0.125  # the left side of the subplots of the figure
    # right = 0.9    # the right side of the subplots of the figure
    # bottom = 0.1   # the bottom of the subplots of the figure
    # top = 0.9      # the top of the subplots of the figure
    # wspace = 0.2   # the amount of width reserved for blank space between subplots
    # hspace = 0.2   # the amount of height reserved for white space between subplots

    gs = gridspec.GridSpec(4, 1,
                           width_ratios=[1],
                           height_ratios=[5, 1, 1, 5]
                           )

    # gs.hspace = 0
    # gs.wspace = 0

    fig = plt.figure(figsize=(3, 3))

    ax_map = plt.subplot(gs[0])
    ax_prof = plt.subplot(gs[1])
    ax_stat = plt.subplot(gs[2])
    ax_3d = plt.subplot(gs[3], projection='3d')

    # fig, ax = plt.subplots()
    # ax2 = fig.add_subplot(gs[0])
    # ax4 = fig.add_subplot(gs[1])
    # ax5 = fig.add_subplot(gs[2])
    #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0)

    # gpxData = GeoSectionGpxPoints("2014_11_17_Bieszczady.gpx")
    # gpxViewerProfile = GeoSectionViewerProfile(ax_prof, gpxData)
    # gpxViewerMap = GeoSectionViewerMap(ax_map, gpxData)
    # gpx3dPath = GeoSectionViewer3d(ax_3d, gpxData)

    #plt.axis('off')
    #plt.savefig("report.png")
    plt.savefig("report.pdf", format='pdf')
    plt.show()

    #-------------
    gpxData = GeoSectionGpxPoints("2014_11_17_Bieszczady.gpx")

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,1,1)
    gpxViewerProfile = GeoSectionViewerProfile(ax1, gpxData)
    fig1.savefig("fig1.png")

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1,1,1)
    gpxViewerMap = GeoSectionViewerMap(ax2, gpxData)
    fig2.savefig("fig2.png", bbox_inches='tight')

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(1,1,1, projection='3d')
    gpx3dPath = GeoSectionViewer3d(ax3, gpxData)
    fig3.savefig("fig3.png")

    gs = gridspec.GridSpec(3, 1)
    fig4 = plt.figure(figsize=(10, 10))
    ax_im_1 = fig4.add_subplot(gs[0])
    ax_im_2 = fig4.add_subplot(gs[1])
    ax_im_3 = fig4.add_subplot(gs[2])
    img1 = mpimg.imread('fig1.png')
    img2 = mpimg.imread('fig2.png')
    img3 = mpimg.imread('fig3.png')
    ax_im_1.imshow(img1)
    ax_im_2.imshow(img2)
    ax_im_3.imshow(img3)
    fig4.savefig("fig4.png", bbox_inches='tight')

    import markdown

    html = markdown.markdown("asdasdasd")

    from string import Template

    fIn = open('gpxReport.tpl', 'r')
    template = Template(fIn.read())
    d = dict(Title = "Bieszczady", FigProfile = "Res/fig1.png", FigMap = "Res/fig2.png", Fig3d = "Res/fig3.png", GpxFile = "Res/bieszczady.gpx")
    output = template.substitute(d)
    print(output)
    fOut = open('/home/ziemek/Projects/pooleTestProj/input/gpxReport.md', 'w')
    fOut.write(output)
    fOut.close()

    # import matplotlib.pyplot as plt
    #
    # def main():
    #     fig = plt.figure()
    #     plt.axis([0, 10, 0, 10])
    #
    #     t = "This is a really long string that I'd rather have wrapped so that it"\
    #     " doesn't go outside of the figure, but if it's long enough it will go"\
    #     " off the top or bottom!"
    #     plt.text(4, 1, t, ha='left', rotation=15)
    #     plt.text(5, 3.5, t, ha='right', rotation=-15)
    #     plt.text(5, 10, t, fontsize=18, ha='center', va='top')
    #     plt.text(3, 0, t, family='serif', style='italic', ha='right')
    #     plt.title("This is a really long title that I want to have wrapped so it"\
    #              " does not go outside the figure boundaries", ha='center')
    #
    #     # Now make the text auto-wrap...
    #     fig.canvas.mpl_connect('draw_event', on_draw)
    #
    #     plt.savefig('text.png')
    #     plt.show()
    #
    # def on_draw(event):
    #     """Auto-wraps all text objects in a figure at draw-time"""
    #     import matplotlib as mpl
    #     fig = event.canvas.figure
    #
    #     # Cycle through all artists in all the axes in the figure
    #     for ax in fig.axes:
    #         for artist in ax.get_children():
    #             # If it's a text artist, wrap it...
    #             if isinstance(artist, mpl.text.Text):
    #                 autowrap_text(artist, event.renderer)
    #
    #     # Temporarily disconnect any callbacks to the draw event...
    #     # (To avoid recursion)
    #     func_handles = fig.canvas.callbacks.callbacks[event.name]
    #     fig.canvas.callbacks.callbacks[event.name] = {}
    #     # Re-draw the figure..
    #     fig.canvas.draw()
    #     # Reset the draw event callbacks
    #     fig.canvas.callbacks.callbacks[event.name] = func_handles
    #
    # def autowrap_text(textobj, renderer):
    #     """Wraps the given matplotlib text object so that it exceed the boundaries
    #     of the axis it is plotted in."""
    #     import textwrap
    #     # Get the starting position of the text in pixels...
    #     x0, y0 = textobj.get_transform().transform(textobj.get_position())
    #     # Get the extents of the current axis in pixels...
    #     clip = textobj.get_axes().get_window_extent()
    #     # Set the text to rotate about the left edge (doesn't make sense otherwise)
    #     textobj.set_rotation_mode('anchor')
    #
    #     # Get the amount of space in the direction of rotation to the left and
    #     # right of x0, y0 (left and right are relative to the rotation, as well)
    #     rotation = textobj.get_rotation()
    #     right_space = min_dist_inside((x0, y0), rotation, clip)
    #     left_space = min_dist_inside((x0, y0), rotation - 180, clip)
    #
    #     # Use either the left or right distance depending on the horiz alignment.
    #     alignment = textobj.get_horizontalalignment()
    #     if alignment is 'left':
    #         new_width = right_space
    #     elif alignment is 'right':
    #         new_width = left_space
    #     else:
    #         new_width = 2 * min(left_space, right_space)
    #
    #     # Estimate the width of the new size in characters...
    #     aspect_ratio = 0.5 # This varies with the font!!
    #     fontsize = textobj.get_size()
    #     pixels_per_char = aspect_ratio * renderer.points_to_pixels(fontsize)
    #
    #     # If wrap_width is < 1, just make it 1 character
    #     wrap_width = max(1, new_width // pixels_per_char)
    #     try:
    #         wrapped_text = textwrap.fill(textobj.get_text(), wrap_width)
    #     except TypeError:
    #         # This appears to be a single word
    #         wrapped_text = textobj.get_text()
    #     textobj.set_text(wrapped_text)
    #
    # def min_dist_inside(point, rotation, box):
    #     """Gets the space in a given direction from "point" to the boundaries of
    #     "box" (where box is an object with x0, y0, x1, & y1 attributes, point is a
    #     tuple of x,y, and rotation is the angle in degrees)"""
    #     from math import sin, cos, radians
    #     x0, y0 = point
    #     rotation = radians(rotation)
    #     distances = []
    #     threshold = 0.0001
    #     if cos(rotation) > threshold:
    #         # Intersects the right axis
    #         distances.append((box.x1 - x0) / cos(rotation))
    #     if cos(rotation) < -threshold:
    #         # Intersects the left axis
    #         distances.append((box.x0 - x0) / cos(rotation))
    #     if sin(rotation) > threshold:
    #         # Intersects the top axis
    #         distances.append((box.y1 - y0) / sin(rotation))
    #     if sin(rotation) < -threshold:
    #         # Intersects the bottom axis
    #         distances.append((box.y0 - y0) / sin(rotation))
    #     return min(distances)

