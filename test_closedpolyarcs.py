
import pygmaps as pgm

mymap = pgm.maps(37.430, -122.145, 17)

# An arc is characterized by the tuple:
# (lat, lon, rad, thi, thf, color, addmarder, markertitle)
#
# lat: circle center's latitude.
# lon: circle center's longitude.
# rad: circle's radius.
# thi: initial arc angle as measured from the center's latitude.
# thf: final arc angle as measured from the center's latitude.
# color: arc's color.
# addmarder: boolean to decide if add a marker to the circle's center or not.
# markertitle: text shown as your mouse hover over the marker.
#
# Note also that an arc is a subset of a circle or cicumference.

# In the case of a closed polyarc the color is chosen separatetely. 
# So a closed polyarc is a list of arcs where the color is overwritten 
# for the whole path of arcs. The list of arcs should be return to the 
# same point, otherwise a path between the first and last points will be 
# drawn to close the list of arcs.

closedpolyarc1 = [
(37.427, -122.147, 193, 0, 90, '#FF0000', True, 'First arc of closed polyarc1!'),
(37.430, -122.147, 140, 270, 180, '#0000FF', True, 'Second arc of closed polyarc1!'),
]
mymap.addclosedpolyarc(closedpolyarc1)

closedpolyarc2 = [
(37.430, -122.143, 140, -30, 60, '#FF0000', True, 'First arc of closed polyarc2!'),
(37.428, -122.143, 350, 80, 120, '#0000FF', True, 'Second arc of closed polyarc2!'),
]
mymap.addclosedpolyarc(closedpolyarc2, color = '#FF0000')

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_closedpolyarcs.html', 'w')
f.write(myhtml_map)
f.close()

