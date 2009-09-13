import hardware.gps
import map.source
import time


class PyGPS(object):
    """ Represents the main application.
    """
    def __init__(self):
        self.gps = hardware.gps.GPSMiniMicro()
        self.map_src = map.source.GoogleMap()
        self.run()
        
    def run(self):        
        while True:
            self.gps.update_coordinates()
            img = self.map_src.get_img(self.gps.lat, self.gps.lng, 200, 200)
            f = open('img.gif', 'wb')
            f.write(img)
            f.close()
            print self.gps.lat, self.gps.lng
            time.sleep(10)

if __name__ == '__main__':
#    port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")
    PyGPS()