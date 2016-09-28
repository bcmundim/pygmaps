
import pygmaps as pgm

mymap = pgm.maps(37.428, -122.145, 16)

mymap.addpoint(37.427, -122.145, "#0000FF")

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_point.html', 'w')
f.write(myhtml_map)
f.close()

