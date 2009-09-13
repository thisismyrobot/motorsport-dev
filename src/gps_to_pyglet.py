import serial
import BaseHTTPServer
import json
import webbrowser


class HandleRequest(BaseHTTPServer.BaseHTTPRequestHandler):
    """ This class handles incoming requests to the server and accepts
        two different GET requests "/gps" and "/map". The "/gps" request
        triggers the generation of a json bundle holding the latest gps
        coordinates. The "/map" request triggers the passing-through
        of the map.html, which displays the google map and peforms the "/gps"
        requests to center the map over the current location.
    """
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
    """ returns the current gps coordinate as json. it ignores any failures
        which is not ideal...
    """
    try:
        line = [""]
        #wait for the desired gps data line
        while line[0] != "$GPRMC":
            line = conn.readline().split(',')

        #extract the longtitude and latitude
        lon_gps = line[3]
        lat_gps = line[5]

        #convert from DDMM.MMMM -> DD.DDDDDD
        lon_d = float(lon_gps[0:2]) + (float(lon_gps[2:]) / 60)
        lat_d = float(lat_gps[0:3]) + (float(lat_gps[3:]) / 60)

        #detect polarity using NS/EW values
        if line[4] == 'S':
            lon_d = -lon_d
        if line[6] == 'W':
            lat_d = -lat_d

        #create json and return to client
        json_data = json.dumps((lon_d, lat_d))
        return json_data
    except:
        pass

def start_server(server_class=BaseHTTPServer.HTTPServer):
    """ Starts a basic http server, assignes a request handler.
    """
    server_address = ('', 80)
    httpd = server_class(server_address, HandleRequest)
    httpd.serve_forever()

if __name__ == '__main__':
    port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")
    conn = serial.Serial(port, 4800, timeout=2)
    webbrowser.open("http://localhost/map")
    start_server()
