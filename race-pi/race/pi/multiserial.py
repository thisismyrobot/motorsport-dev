""" Serial port multiplexer.
"""
import multiprocessing
import Queue
import serial.tools.list_ports
import time


def reader(queue, path, newport):
    """Process to read from a comm port and put lines on a queue."""
    try:

        # Connect at 9600 baud
        conn = serial.Serial(path, timeout=1)

        # Perform and post-creation commands
        newport(conn)

        # Push data on to the queue
        while True:
            queue.put(':'.join((path, conn.readline())))

    except:
        time.sleep(1)
        return


def writer(data_queue, write_queue, outs):
    """Process to read from a queue."""
    conns = []
    for kwargs in outs:
        kwargs.update({'timeout': 1})
        conns.append(serial.Serial(**kwargs))

    while True:
        line = data_queue.get()
        try:
            if write_queue is not None:
                write_queue.put(line, block=False)
        except Queue.Full:
            # Not all implementations read from it quick enough. This
            # shouldn't be terminal.
            pass
        for conn in conns:
            conn.write(line)


def run(outs, ins_filter='/dev/ttyUSB.*', newport=lambda conn: None, write_queue=None):
    """Multiplex RX from a number of serial ports to one or more TX ports.

    Assumes all input ports are 9600 baud, sorry.

    Params:
        * outs: a list of dicts containing kwargs for serial.Serial.
        * ins_filter: an (optional) regex filter for the serial ports to read
          from.
        * newport: an (optional) function to call with the open serial
          connection as the only argument. Use to set up serial devices.
        * write_queue: an (optional) multiprocessing.Queue to echo all serial
          data to.
    """
    data_queue = multiprocessing.Queue()

    multiprocessing.Process(
        target=writer,
        args=(data_queue, write_queue, outs)
    ).start()

    readers = {}

    while True:

        for (path, _, _) in serial.tools.list_ports.grep(ins_filter):

            if path not in readers.keys() or not readers[path].is_alive():

                readers[path] = multiprocessing.Process(
                    target=reader, args=(data_queue, path, newport)
                )
                readers[path].start()
