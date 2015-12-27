import led
import serial


ser = serial.Serial('/dev/ttyAMA0', 4800)#, timeout=1)
led_disp = led.LED()

while True:
    line = ser.readline()
    if line.startswith('$GPVTG'):
        kph = line.split(',')[7]
        if kph == '':
            led_disp.set('NO GPS')
        else:
            led_disp.set('{} kph'.format(kph))
