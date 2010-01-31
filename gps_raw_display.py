""" simply streams gps data to the console
"""

import serial

port = raw_input("what port do you want (eg: COM9 or /dev/ttyUSB0)")

conn = serial.Serial(port, 4800, timeout=2)

while True:
    line = conn.readline()
    print line