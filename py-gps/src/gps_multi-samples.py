""" simply streams gps data to the console
"""

import serial
import webbrowser

lat_av = []
lng_av = []

port = raw_input("what port do you want (eg: COM1 or /dev/ttyUSB0)?: ")
samples = int(raw_input("how many samples?: "))

conn = serial.Serial(port, 4800, timeout=2)

for i in range(samples):
    line = [""]

    #wait for the desired gps data line
    while line[0] != "$GPRMC":
        line = conn.readline().split(',')

    #check we have a lock
    if line[2] == 'V':
        print "no satellite lock!"
    else:
        #extract the longtitude and latitude
        lon_gps = line[3]
        lat_gps = line[5]

        #convert from DDMM.MMMM -> DD.DDDDDD
        lng_d = float(lon_gps[0:2]) + (float(lon_gps[2:]) / 60)
        lat_d = float(lat_gps[0:3]) + (float(lat_gps[3:]) / 60)

        #detect polarity using NS/EW values
        if line[4] == 'S':
            lng_d = -lng_d
        if line[6] == 'W':
            lat_d = -lat_d

        lat_av.append(lat_d)
        lng_av.append(lng_d)
        
        print samples-i

lat_d = sum(lat_av, 0.0) / len(lat_av)
lng_d = sum(lng_av, 0.0) / len(lng_av)

url = "http://maps.google.com/maps?q=%s %s" % (lng_d, lat_d)
webbrowser.open(url)
print "done!"
raw_input() #naughty way of doing a cross-platform "pause" - press enter to proceed pass