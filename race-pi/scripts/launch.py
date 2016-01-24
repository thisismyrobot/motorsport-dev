""" Main process for running "Race Pi"
"""
import multiprocessing
import os
import pty

import race.pi.multiserial
import race.pi.led


# Set up a helper to write the GPS data to the LED display (and log to the
# console).
def display_update(display, queue):
    while True:
        line = queue.get().strip()
        print line
        if line.startswith('$GPVTG'):
            kph = line.split(',')[7]
            if kph == '':
                display.set('NO LOCK')
            else:
                display.set('{} kph'.format(kph))


if __name__ == '__main__':

    # Create a LED display instance
    display = race.pi.led.LED()
    display.set('NO GPS')

    # Create the logging queue to grab data from the serial lines.
    log_queue = multiprocessing.Queue()
    multiprocessing.Process(
        target=display_update, args=(display, log_queue,)
    ).start()

    # We're using ublox GPS units so we'll set them up after connection here.
    def ublox_setup(conn):
        # Set to work at 5Hz.
        conn.write(b'\xb5\x62\x06\x08\x06\x00\xc8\x00\x01\x00\x01\x00\xde\x6a')

    # Create an pty to send to so that
    paths = map(os.ttyname, pty.openpty())

    # Set up the multi-serial multiplexer, echoing all serial data out the
    # onboard serial port. In my case this is attached to a OpenLog.
    race.pi.multiserial.run(
        outs=(
            # Each dict is kwargs to a serial.Serial instance.
            {'port': '/dev/ttyAMA0'},  # On-board Pi serial.
        ),
        newport=ublox_setup,
        write_queue=log_queue,
    )
