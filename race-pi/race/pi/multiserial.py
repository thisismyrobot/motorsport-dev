""" Serial port multiplexer.
"""
import multiprocessing
import serial
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


def writer(queue, outs):
    """Process to read from a queue."""
    conns = []
    for kwargs in outs:
        kwargs.update({'timeout': 1})
        conns.append(serial.Serial(**kwargs))
        print 'writing to {}'.format(kwargs['port'])

    while True:
        line = queue.get()
        for conn in conns:
            conn.write(line)


def run(outs, ins_filter='/dev/ttyUSB.*', newport=lambda conn: None):
    """Multiplex RX from a number of serial ports to one or more TX ports.

    Assumes all input ports are 9600 baud, sorry.
    """
    queue = multiprocessing.Queue()

    multiprocessing.Process(target=writer, args=(queue, outs)).start()

    readers = {}

    while True:

        for (path, _, _) in serial.tools.list_ports.grep(ins_filter):

            if path not in readers.keys() or not readers[path].is_alive():

                readers[path] = multiprocessing.Process(
                    target=reader, args=(queue, path, newport)
                )
                readers[path].start()
