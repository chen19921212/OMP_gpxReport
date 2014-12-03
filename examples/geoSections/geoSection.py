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

# from __future__ import print_function
# from matplotlib.dates import strpdate2num
# #from matplotlib.mlab import load
# import numpy as np
# from pylab import figure, show
# import matplotlib.cbook as cbook
# import matplotlib.pyplot as plt
#
#
# from examples import gpxpy
#
# gpx_file = open('../aa.gpx', 'r')
# gpx = gpxpy.parse(gpx_file)
# points = gpx.tracks[0].segments[0].points
#
# latitudes = []
# longitudes = []
# elevations = []
# timestamps = []
#
# for point in points:
#     latitudes.append(point.latitude)
#     longitudes.append(point.longitude)
#     elevations.append(point.elevation)
#     timestamps.append(point.time)
#
# #latitude, longitude, elevation time
#
# # datafile = cbook.get_sample_data('msft.csv', asfileobj=False)
# # print('loading', datafile)
# #
# # dates, closes = np.loadtxt(
# #     datafile, delimiter=',',
# #     converters={0:strpdate2num('%d-%b-%y')},
# #     skiprows=1, usecols=(0,2), unpack=True)
# #
# #fig = figure()
# fig = plt.figure()
#
# ax = fig.add_subplot(111)
# ax.plot_date(timestamps, elevations, '-')
# fig.autofmt_xdate()
#
# plt.savefig('elevation.png')
# plt.show()
#
#
# plt.close()

import matplotlib.pyplot as plt

def main():
    fig = plt.figure()
    plt.axis([0, 10, 0, 10])

    t = "This is a really long string that I'd rather have wrapped so that it"\
    " doesn't go outside of the figure, but if it's long enough it will go"\
    " off the top or bottom!"
    plt.text(4, 1, t, ha='left', rotation=15)
    plt.text(5, 3.5, t, ha='right', rotation=-15)
    plt.text(5, 10, t, fontsize=18, ha='center', va='top')
    plt.text(3, 0, t, family='serif', style='italic', ha='right')
    plt.title("This is a really long title that I want to have wrapped so it"\
             " does not go outside the figure boundaries", ha='center')

    # Now make the text auto-wrap...
    fig.canvas.mpl_connect('draw_event', on_draw)

    plt.savefig('text.png')
    plt.show()

def on_draw(event):
    """Auto-wraps all text objects in a figure at draw-time"""
    import matplotlib as mpl
    fig = event.canvas.figure

    # Cycle through all artists in all the axes in the figure
    for ax in fig.axes:
        for artist in ax.get_children():
            # If it's a text artist, wrap it...
            if isinstance(artist, mpl.text.Text):
                autowrap_text(artist, event.renderer)

    # Temporarily disconnect any callbacks to the draw event...
    # (To avoid recursion)
    func_handles = fig.canvas.callbacks.callbacks[event.name]
    fig.canvas.callbacks.callbacks[event.name] = {}
    # Re-draw the figure..
    fig.canvas.draw()
    # Reset the draw event callbacks
    fig.canvas.callbacks.callbacks[event.name] = func_handles

def autowrap_text(textobj, renderer):
    """Wraps the given matplotlib text object so that it exceed the boundaries
    of the axis it is plotted in."""
    import textwrap
    # Get the starting position of the text in pixels...
    x0, y0 = textobj.get_transform().transform(textobj.get_position())
    # Get the extents of the current axis in pixels...
    clip = textobj.get_axes().get_window_extent()
    # Set the text to rotate about the left edge (doesn't make sense otherwise)
    textobj.set_rotation_mode('anchor')

    # Get the amount of space in the direction of rotation to the left and
    # right of x0, y0 (left and right are relative to the rotation, as well)
    rotation = textobj.get_rotation()
    right_space = min_dist_inside((x0, y0), rotation, clip)
    left_space = min_dist_inside((x0, y0), rotation - 180, clip)

    # Use either the left or right distance depending on the horiz alignment.
    alignment = textobj.get_horizontalalignment()
    if alignment is 'left':
        new_width = right_space
    elif alignment is 'right':
        new_width = left_space
    else:
        new_width = 2 * min(left_space, right_space)

    # Estimate the width of the new size in characters...
    aspect_ratio = 0.5 # This varies with the font!!
    fontsize = textobj.get_size()
    pixels_per_char = aspect_ratio * renderer.points_to_pixels(fontsize)

    # If wrap_width is < 1, just make it 1 character
    wrap_width = max(1, new_width // pixels_per_char)
    try:
        wrapped_text = textwrap.fill(textobj.get_text(), wrap_width)
    except TypeError:
        # This appears to be a single word
        wrapped_text = textobj.get_text()
    textobj.set_text(wrapped_text)

def min_dist_inside(point, rotation, box):
    """Gets the space in a given direction from "point" to the boundaries of
    "box" (where box is an object with x0, y0, x1, & y1 attributes, point is a
    tuple of x,y, and rotation is the angle in degrees)"""
    from math import sin, cos, radians
    x0, y0 = point
    rotation = radians(rotation)
    distances = []
    threshold = 0.0001
    if cos(rotation) > threshold:
        # Intersects the right axis
        distances.append((box.x1 - x0) / cos(rotation))
    if cos(rotation) < -threshold:
        # Intersects the left axis
        distances.append((box.x0 - x0) / cos(rotation))
    if sin(rotation) > threshold:
        # Intersects the top axis
        distances.append((box.y1 - y0) / sin(rotation))
    if sin(rotation) < -threshold:
        # Intersects the bottom axis
        distances.append((box.y0 - y0) / sin(rotation))
    return min(distances)

if __name__ == '__main__':
    main()
