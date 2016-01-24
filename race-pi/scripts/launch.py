""" Main process for running "Race Pi"
"""
import multiprocessing
import os
import pty
import serial

import race.pi.multiserial


if __name__ == '__main__':

    # We want to send a 5Hz-enable command to all ports we find.
    def newport(conn):
        conn.write(b'\xb5\x62\x06\x08\x06\x00\xc8\x00\x01\x00\x01\x00\xde\x6a')

    # Create an pty to send to so that
    paths = map(os.ttyname, pty.openpty())

    # Set up a console logger for testing
    def log(port):
        print 'reading from {}'.format(port)
        conn = serial.Serial(port, rtscts=True, dsrdtr=True)
        while True:
            print conn.readline().strip()
    multiprocessing.Process(target=log, args=(paths[0],)).start()

    # Set up the multi-serial multiplexer
    race.pi.multiserial.run(
        outs=(
            {'port': '/dev/ttyAMA0', 'baudrate': 9600},  # On-board Pi serial.
            {'port': paths[1], 'baudrate': 9600, 'rtscts': True, 'dsrdtr': True},  # PTY to get access to the multiplexed data.
        ),
        newport=newport,
    )
