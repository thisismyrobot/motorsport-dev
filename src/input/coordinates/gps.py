import serial


class GPSMiniMicro(object):
    """ Represents the GPS Mini-Micro from SparkFun
    """
    port = "COM9"
    baud = "4800"

    def _get_line_from_unit(self, line_id="$GPRMC"):
        """ handles the retrieval of a line from the unit
        """
        conn = serial.Serial(self.port, self.baud, timeout=2)
        line = [""]
        while line[0] != line_id:
            line = conn.readline().split(',')
        return line

    def update_coordinates(self):
        """ Updates an internal store of the current gps coordinates.
        """
        line = self._get_line_from_unit()

        #extract the longtitude and latitude
        lng_gps = line[3]
        lat_gps = line[5]

        #convert from DDMM.MMMM -> DD.DDDDDD
        #lng_d = float(lng_gps[0:2]) + (float(lng_gps[2:]) / 60)
        #lat_d = float(lat_gps[0:3]) + (float(lat_gps[3:]) / 60)

        #convert DD.DDDDDD -> DDDDDDDD (for google maps)
        #lng_d = str(lng_d).replace(".","")
        #lat_d = str(lat_d).replace(".","")

#        print lng_d, lat_d
        #detect polarity using NS/EW values
#        if line[4] == 'S':
#            lng_d = -lng_d
#        if line[6] == 'W':
#            lat_d = -lat_d

        #update self
        self.lat = lat_gps.replace(".","")
        self.lng = lng_gps.replace(".","")