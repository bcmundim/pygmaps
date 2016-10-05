
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

mymap.addarc( 37.429, -122.145, 193, thi = 0, thf = 90, color = '#0000FF', 
              addmarker = True, markertitle = 'First arc!')

mymap.addarc( 37.430, -122.143, 140, thi = -30, thf = 60, color = '#FF0000', 
              addmarker = True, markertitle = 'Second arc!')



# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_arcs.html', 'w')
f.write(myhtml_map)
f.close()

