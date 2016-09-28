
import pygmaps as pgm

mymap = pgm.maps(37.428, -122.145, 16)

path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
mymap.addpath(path,"#00FF00")

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_path.html', 'w')
f.write(myhtml_map)
f.close()

