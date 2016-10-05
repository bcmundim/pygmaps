
import pygmaps as pgm

mymap = pgm.maps(37.428, -122.145, 16)

path1 = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
mymap.addpath(path1,"#00FF00")

path2 = [(37.430, -122.143),(37.432, -122.141),(37.430, -122.139)]
mymap.addpath(path2,"#FF0000")

# Return the html document as a string:
myhtml_map = mymap.draw(ToFile = False)
f = open('./test/test_paths.html', 'w')
f.write(myhtml_map)
f.close()

