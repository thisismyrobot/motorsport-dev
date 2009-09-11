import serial

port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")

conn = serial.Serial(port, 4800, timeout=2)

while True:
    line = conn.readline().split(',')
    if line[0] == "$GPRMC":
        lat = line[3]
        long = line[5]
        lat_s = "-%d %.4f" % (int(lat[0:2]), float(lat[2:]))
        long_s = "%d %.4f" % (int(long[0:3]), float(long[3:]))
        print "%s %s" % (lat_s, long_s)