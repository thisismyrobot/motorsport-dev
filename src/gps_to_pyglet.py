import input.coordinates.gps
import input.map.network
import output.visual.opengl
import time


class PyGPS(object):
    """ Represents the main application.
    """
    def __init__(self):
        self.display = output.visual.opengl.IsoRenderer()
        self.gps = input.coordinates.gps.GPSMiniMicro()
        self.map_src = input.map.network.GoogleMap()
        self.run()
        
    def run(self):        
        self.gps.update_coordinates()
        img = self.map_src.get_img(self.gps.lat, self.gps.lng, 1024, 1024)
        f = open('img.gif', 'wb')
        f.write(img)
        f.close()

        while True:
            self.display.render()
#            print self.gps.lat, self.gps.lng
#            time.sleep(10)

if __name__ == '__main__':
#    port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")
    PyGPS()