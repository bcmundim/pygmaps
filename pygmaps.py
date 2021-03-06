import math
import os
###########################################################
## Google map python wrapper V0.1
## 
############################################################

class return_string:
    """
        Class to overwrite the file object open to draw the map.
        Return the whole html as a string to be further processed if needed.
    """
    def __init__(self):
        self.string = ""
        self.slist = []

    def write(self, newstring):
        self.slist.append(newstring)

    def close(self):
        self.string = "".join(self.slist)


class maps:

   def __init__(self, centerLat, centerLng, zoom ):
      self.center = (float(centerLat),float(centerLng))
      self.zoom = int(zoom)
      self.grids = None
      self.paths = []
      self.points = []
      self.radpoints = []
      self.arcs = []
      self.polyarcs = []
      self.closedpolyarcs = []
      self.gridsetting = None
      self.coloricon = 'http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,XXXXXX,000000&ext=.png'

   def setgrids(self,slat,elat,latin,slng,elng,lngin):
      self.gridsetting = [slat,elat,latin,slng,elng,lngin]

   def addpoint(self, lat, lng, color = '#FF0000', 
                markertitle = "Not available at the moment"):
      self.points.append((lat,lng,color[1:],markertitle))

   #def addpointcoord(self, coord):
   #   self.points.append((coord[0],coord[1]))

   def addradpoint(self, lat,lng,rad,color = '#0000FF', fill = False, addmarker = False,
                   markertitle = "Not available at the moment"):
      self.radpoints.append((lat,lng,rad, 0, 360, color,fill,addmarker,markertitle))

   def addarc(self, lat, lng, rad, thi = 0, thf = 360, color = '#0000FF', 
              addmarker = False, markertitle = "Not available at the moment"):
      self.arcs.append((lat,lng,rad,thi,thf,color,addmarker,markertitle))

#   def addpolyarc(self, lat, lng, rad, thi = 0, thf = 360, color = '#0000FF', 
#              addmarker = False, markertitle = "Not available at the moment"):
#      self.polyarcs.append((lat,lng,rad,thi,thf,color,addmarker,markertitle))

   def addpolyarc(self, polyarc, color = '#0000FF'):
      self.polyarcs.append((polyarc,color))

   def addclosedpolyarc(self, closedpolyarc, color = '#0000FF'):
      self.closedpolyarcs.append((closedpolyarc,color))

   def addpath(self,path,color = '#FF0000'):
      path.append(color)
      self.paths.append(path)
   
   # Create the html document, which includes one google map and all points 
   # and paths, and write it to file or return it as a string to be further
   # processed by other applications.
   def draw(self, htmldoc = "mymap_draw_test.html", apikey = "", ToFile = True,
            title = "Google Maps - pygmaps"):
      if ToFile:
        f = open(htmldoc,'w')
      else:
        f = return_string()
      
      f.write('<!DOCTYPE html>\n')
      f.write('<html>\n')
      f.write('<head>\n')
      f.write('<meta name="viewport" content="initial-scale=1.0">\n')
      f.write('<meta charset=utf-8">\n')
      f.write('<title>%s</title>\n'% (title))
      f.write('<style>\n')
      f.write('\thtml, body {\n')
      f.write('\t\theight: 100%;\n')
      f.write('\t\tmargin: 0;\n')
      f.write('\t\tpadding: 0;\n')
      f.write('\t}\n')
      f.write('\t#map_canvas {\n')
      f.write('\t\theight: 100%;\n')
      f.write('\t}\n')
      f.write('</style>\n')
      f.write('</head>\n')
      f.write('<body>\n')
      #f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
      f.write('\t<div id="map_canvas"></div>\n')

      f.write('<script>\n')
      f.write('\tvar map;\n')
      f.write('\tfunction initialize() {\n')
      self.drawmap(f)
      self.drawgrids(f)
      self.drawpoints(f)
      self.drawradpoints(f)
      self.drawarcs(f)
      self.drawpolyarcs(f)
      self.drawclosedpolyarcs(f)
      self.drawpaths(f,self.paths)
      f.write('\t}\n')
      f.write('</script>\n')

      f.write('<script src="https://maps.googleapis.com/maps/api/js?key=')
      f.write(apikey)
      f.write('&callback=initialize" async defer></script>\n')

      f.write('</body>\n')
      f.write('</html>\n')
      f.close()
      if not ToFile:
        return f.string

   def drawgrids(self, f):
      if self.gridsetting == None:
         return
      slat = self.gridsetting[0]
      elat = self.gridsetting[1]
      latin = self.gridsetting[2]
      slng = self.gridsetting[3]
      elng = self.gridsetting[4]
      lngin = self.gridsetting[5]
      self.grids = []

      r = [slat+float(x)*latin for x in range(0, int((elat-slat)/latin))]
      for lat in r:
         self.grids.append([(lat+latin/2.0,slng+lngin/2.0),(lat+latin/2.0,elng+lngin/2.0)])

      r = [slng+float(x)*lngin for x in range(0, int((elng-slng)/lngin))]
      for lng in r:
         self.grids.append([(slat+latin/2.0,lng+lngin/2.0),(elat+latin/2.0,lng+lngin/2.0)])
      
      for line in self.grids:
         self.drawPolyline(f,line,strokeColor = "#000000")

   def drawpoints(self,f):
      for point in  self.points:
         self.drawpoint(f,point[0],point[1],point[2],point[3])

   def drawradpoints(self, f):
      for rpoint in self.radpoints:
         path = self.getcycle(rpoint[0:5])
         # if addmarker:
         if rpoint[7]:
            # lat, lon, color, markertitle:
            self.drawpoint(f,rpoint[0],rpoint[1],rpoint[5],rpoint[8])
         # fill == rpoint[4]:
         if rpoint[6]:
            self.drawPolygon(f,path,strokeColor = rpoint[5], 
                             fillColor = rpoint[5], fillOpacity = 0.1)
         else:
            self.drawPolygon(f,path,strokeColor = rpoint[5])

#                         0   1   2   3   4    5     6      7         8
# self.radpoints.append((lat,lng,rad, 0, 360, color,fill,addmarker,markertitle))
#                    0   1   2   3   4    5      6          7
# self.arcs.append((lat,lng,rad,thi,thf,color,addmarker,markertitle))

   def drawarcs(self, f):
      for arc in self.arcs:
         path = self.getcycle(arc[0:5])
         # if addmarker:
         if arc[6]:
            # lat, lon, color, markertitle:
            self.drawpoint(f,arc[0], arc[1], arc[5], arc[7])
         self.drawPolyline(f,path, strokeColor = arc[5])

   def drawpolyarcs(self, f):
      for parc, color in self.polyarcs:
         path = []
         for arc in parc:
            path += self.getcycle(arc[0:5])
            # if addmarker:
            if arc[6]:
               # lat, lon, color, markertitle:
               self.drawpoint(f,arc[0], arc[1], arc[5], arc[7])
         self.drawPolyline(f,path, strokeColor = color)

   def drawclosedpolyarcs(self, f):
      for parc, color in self.closedpolyarcs:
         path = []
         for arc in parc:
            path += self.getcycle(arc[0:5])
            # if addmarker:
            if arc[6]:
               # lat, lon, color, markertitle:
               self.drawpoint(f,arc[0], arc[1], arc[5], arc[7])
         self.drawPolygon(f,path, strokeColor = color,
                             fillColor = color, fillOpacity = 0.1)

#   def drawpolyarcs(self, f):
#      path = []
#      for arc in self.polyarcs:
#         path += self.getcycle(arc[0:5])
#         # if addmarker:
#         if arc[6]:
#            # lat, lon, color, markertitle:
#            self.drawpoint(f,arc[0], arc[1], arc[5], arc[7])
#
#      self.drawPolygon(f,path, strokeColor = "#0000FF",
#                             fillColor = "#0000FF", fillOpacity = 0.1)


   def getcycle(self,rpoint):
      cycle = []
      lat = rpoint[0]
      lng = rpoint[1]
      rad = rpoint[2] # radius in meters

      thi = rpoint[3] # initial angle theta in degrees
      thf = rpoint[4] # final angle theta in degrees
      dtheta = thf - thi
      adtheta = abs(dtheta)
      if adtheta <= 90:
         irange = 9
      elif adtheta <= 180:
         irange = 18
      elif adtheta <= 270:
         irange = 27
      else:
         irange = 36
      hth = dtheta/irange

      # Normalize by Earth's equatorial radius used by Google Maps API.
      # This computes the angle d corresponding to the arc length rad.
      d = rad/6378137.0; # Earth's radius in meters.
      lat1 = (math.pi/180.0)* lat
      lng1 = (math.pi/180.0)* lng

      if int(adtheta) == 360:
         r = [i*10 for i in xrange(36)]
      else:
         r = [thi + i*hth for i in xrange(irange+1)]

      # correcting phase for formula below. TODO: fix the formula!
      ph0 = -90*(math.pi/180.0)
      for a in r:
         tc = (math.pi/180.0)*a + ph0;
         # y = math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(tc))
         # dlng = math.atan2(math.sin(tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(y))
         y = math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(tc))
         dlng = math.atan2(math.sin(tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(y))
         x = ((lng1-dlng+math.pi) % (2.0*math.pi)) - math.pi 
         cycle.append( ( float(y*(180.0/math.pi)),float(x*(180.0/math.pi)) ) )
      return cycle

   def drawpaths(self, f, paths):
      for path in paths:
         #print path
         self.drawPolyline(f,path[:-1], strokeColor = path[-1])

   #############################################
   # # # # # # Low level Map Drawing # # # # # # 
   #############################################
   def drawmap(self, f):
      f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
      f.write('\t\tvar myOptions = {\n')
      f.write('\t\t\tzoom: %d,\n' % (self.zoom))
      f.write('\t\t\tcenter: centerlatlng,\n')
      f.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
      f.write('\t\t};\n')
      f.write('\t\tmap = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
      f.write('\n')



   def drawpoint(self,f,lat,lon,color,markertitle):
      f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
      f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
      f.write('\t\tvar marker = new google.maps.Marker({\n')
      f.write('\t\ttitle: "%s",\n' % (markertitle))
      f.write('\t\ticon: img,\n')
      f.write('\t\tposition: latlng\n')
      f.write('\t\t});\n')
      f.write('\t\tmarker.setMap(map);\n')
      f.write('\n')
      
   def drawPolyline(self,f,path,\
         clickable = False, \
         geodesic = True,\
         strokeColor = "#FF0000",\
         strokeOpacity = 1.0,\
         strokeWeight = 2
         ):
      f.write('var PolylineCoordinates = [\n')
      for coordinate in path:
         f.write('new google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
      f.write('];\n')
      f.write('\n')

      f.write('var Path = new google.maps.Polyline({\n')
      f.write('clickable: %s,\n' % (str(clickable).lower()))
      f.write('geodesic: %s,\n' % (str(geodesic).lower()))
      f.write('path: PolylineCoordinates,\n')
      f.write('strokeColor: "%s",\n' %(strokeColor))
      f.write('strokeOpacity: %f,\n' % (strokeOpacity))
      f.write('strokeWeight: %d\n' % (strokeWeight))
      f.write('});\n')
      f.write('\n')
      f.write('Path.setMap(map);\n')
      f.write('\n\n')

   def drawPolygon(self,f,path,\
         clickable = False, \
         geodesic = True,\
         fillColor = "#000000",\
         fillOpacity = 0.0,\
         strokeColor = "#FF0000",\
         strokeOpacity = 1.0,\
         strokeWeight = 1
         ):
      f.write('var coords = [\n')
      for coordinate in path:
         f.write('new google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
      f.write('];\n')
      f.write('\n')

      f.write('var polygon = new google.maps.Polygon({\n')
      f.write('clickable: %s,\n' % (str(clickable).lower()))
      f.write('geodesic: %s,\n' % (str(geodesic).lower()))
      f.write('fillColor: "%s",\n' %(fillColor))
      f.write('fillOpacity: %f,\n' % (fillOpacity))
      f.write('paths: coords,\n')
      f.write('strokeColor: "%s",\n' %(strokeColor))
      f.write('strokeOpacity: %f,\n' % (strokeOpacity))
      f.write('strokeWeight: %d\n' % (strokeWeight))
      f.write('});\n')
      f.write('\n')
      f.write('polygon.setMap(map);\n')
      f.write('\n\n')

if __name__ == "__main__":

   ########## CONSTRUCTOR: pygmaps.maps(latitude, longitude, zoom) #############
   # DESC:         initialize a map  with latitude and longitude of center 
   #               point and map zoom level "15"
   # PARAMETER1:   latitude (float) latittude of map center point
   # PARAMETER2:   longitude (float) latittude of map center point
   # PARAMETER3:   zoom (int)  map zoom level 0~20
   # RETURN:       the instance of pygmaps
   #============================================================================
   mymap = maps(37.428, -122.145, 16)


   ########## FUNCTION: setgrids(start-Lat, end-Lat, Lat-interval, start-Lng, 
   ##########                    end-Lng, Lng-interval) ########################
   # DESC:         set grids on map  
   # PARAMETER1:   start-Lat (float), start (minimum) latittude of the grids
   # PARAMETER2:   end-Lat (float), end (maximum) latittude of the grids
   # PARAMETER3:   Lat-interval (float)  grid size in latitude 
   # PARAMETER4:   start-Lng (float), start (minimum) longitude of the grids
   # PARAMETER5:   end-Lng (float), end (maximum) longitude of the grids
   # PARAMETER6:   Lng-interval (float)  grid size in longitude 
   # RETURN:       no returns
   #============================================================================
   mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)


   ########## FUNCTION:  addpoint(latitude, longitude, [color]) ################
   # DESC:         add a point into a map and dispaly it, color is optional 
   #               default is red
   # PARAMETER1:   latitude (float) latitude of the point
   # PARAMETER2:   longitude (float) longitude of the point
   # PARAMETER3:   color (string) color of the point showed in map, using HTML 
   #               color code
   # HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
   #                   e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
   # RETURN:       no return
   #============================================================================
   mymap.addpoint(37.427, -122.145, "#0000FF")


   ########## FUNCTION:  addradpoint(latitude, longitude, radius, [color],
   ##########            [fill], [addmarker], [markertitle])               #####
   # DESC:         add a point with a radius (Meter) - Draw cycle
   # PARAMETER1:   latitude (float) latitude of the point
   # PARAMETER2:   longitude (float) longitude of the point
   # PARAMETER3:   radius (float), radius  in meter 
   # PARAMETER4:   color (string) color of the point showed in map, using HTML 
   #               color code
   # HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
   #                   e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
   # PARAMETER5:   fill the circle with the same color stroke but lower opacity.
   # PARAMETER6:   addmarker option to add a marker at the circle center or not.
   # PARAMETER7:   markertitle option string describing the marker.
   # RETURN:       no return 
   #============================================================================
   mymap.addradpoint(37.429, -122.145, 95, "#FF0000", fill = True,
                     addmarker = True,
                     markertitle = "Information about this marker" )


   ########## FUNCTION:  addpath(path,[color]) #################################
   # DESC:         add a path into map, the data struceture of Path is a list 
   #               of points
   # PARAMETER1:   path (list of coordinates) e.g. [(lat1,lng1),(lat2,lng2),...]
   # PARAMETER2:   color (string) color of the point showed in map, using HTML 
   #               color code
   # HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
   #                   e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
   # RETURN:       no return
   #============================================================================
   path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
   mymap.addpath(path,"#00FF00")


   mymap.addarc(37.431, -122.145, 80, thi = 0, thf = 90, color = '#0000FF', 
              addmarker = True, markertitle = "My arc!")


   ########## FUNCTION:  draw(file, [apikey], [ToFile]) ########################
   # DESC:         create the html map file (.html) or returns it as a string.
   # PARAMETER1:   file (string): the map path and file
   # PARAMETER2:   apikey: Optional Google maps API key
   # PARAMETER3:   ToFile: Optional boolean to make it write to file, 
   #               True (default) or return the html doc as a string, False.
   # RETURN:       no return, generate html file in specified directory
   #               or return a string according to PARAMTER3 setting.
   #============================================================================
   mymap.draw('./test/mymap.html')

   # To get your Google maps API key, follow the instructions at 
   # https://developers.google.com/maps/documentation/javascript/get-api-key
   # Save it outside the source code directory. Load it as a environment 
   # variable.
   #apikey = os.environ['YOUR_GOOGLE_MAPS_API_KEY']
   apikey = 'YOUR_GOOGLE_MAPS_API_KEY' 
   mymap.draw('./test/mymap_with_API_key.html', apikey = apikey)

   # Return the html document as a string:
   mymap_string_html = mymap.draw(title = "My title", ToFile = False)
   f = open('./test/mymap_string_html.html', 'w')
   f.write(mymap_string_html)
   f.close()

