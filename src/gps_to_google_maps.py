import serial
import BaseHTTPServer
import json
import webbrowser


port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")
conn = serial.Serial(port, 4800, timeout=2)

class HandleRequest(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == "/gps":
            self.wfile.write(update_gps_data())
        elif self.path == "/map":   
            mapfile = open('map.html').read()
            self.wfile.write(mapfile)


def update_gps_data():
    """ returns the current gps coordinate as json
    """
    try:
        line = [""]
        while line[0] != "$GPRMC":
            line = conn.readline().split(',')
        lon_gps = line[3]
        lat_gps = line[5]

        #convert from DDMM.MMMM -> DD.DDDDDD
        lon_d = float(lon_gps[0:2]) + (float(lon_gps[2:]) / 60)
        lat_d = float(lat_gps[0:3]) + (float(lat_gps[3:]) / 60)

        if line[4] == 'S':
            lon_d = -lon_d
        if line[6] == 'W':
            lat_d = -lat_d
        coord = "%s\n%s" % (lon_d, lat_d)
        json_data = json.dumps((lon_d, lat_d))
        #print "%s, %s" % (lon_d, lat_d)
        return json_data
    except:
        pass

def start_server(server_class=BaseHTTPServer.HTTPServer):
    server_address = ('', 80)
    httpd = server_class(server_address, HandleRequest)
    httpd.serve_forever()

if __name__ == '__main__':
    webbrowser.open("http://localhost/map")
    start_server()
