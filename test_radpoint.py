
import pygmaps as pgm

mymap = pgm.maps(37.428, -122.145, 16)

mymap.addradpoint(37.429, -122.145, 95, "#FF0000", fill = True,
                  addmarker = True,
                  markertitle = "Information about this marker" )

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_radpoint.html', 'w')
f.write(myhtml_map)
f.close()

