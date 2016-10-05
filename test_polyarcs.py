
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

# In the case of a polyarc the color is chosen separatetely. So a polyarc
# is a list of arcs where the color is overwritten for the whole path of arcs.

polyarc1 = [
(37.429, -122.145, 193, 0, 90, '#FF0000', True, 'First arc of polyarc1!'),
(37.432, -122.145, 140, 270, 180, '#0000FF', True, 'Second arc of polyarc1!'),
]
mymap.addpolyarc(polyarc1)

polyarc2 = [
(37.430, -122.143, 140, -30, 60, '#FF0000', True, 'First arc of polyarc2!'),
(37.428, -122.143, 350, 80, 120, '#0000FF', True, 'Second arc of polyarc2!'),
]
mymap.addpolyarc(polyarc2, color = '#FF0000')

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_polyarcs.html', 'w')
f.write(myhtml_map)
f.close()

