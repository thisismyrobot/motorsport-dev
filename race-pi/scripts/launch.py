""" Main process for running "Race Pi"
"""
import multiprocessing
import os
import pty

import race.pi.multiserial


if __name__ == '__main__':

    # We're using ublox GPS units so we'll set them up after connection here.
    def ublox_setup(conn):
        # Set to work at 5Hz.
        conn.write(b'\xb5\x62\x06\x08\x06\x00\xc8\x00\x01\x00\x01\x00\xde\x6a')

    # Create an pty to send to so that
    paths = map(os.ttyname, pty.openpty())

    # Set up a console logger for testing
    def log(queue):
        while True:
            print queue.get().strip()
    log_queue = multiprocessing.Queue()
    multiprocessing.Process(target=log, args=(log_queue,)).start()

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
