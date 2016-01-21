import multiprocessing
import serial.tools.list_ports
import time


def reader(queue, path):
    """ Process to read from a comm port and put lines on a queue.
    """
    # Connect at 9600 baud
    conn = serial.Serial(path, timeout=1)

    # Push data on to the queue.
    while True:
        # Check we have a GPS device
        line = conn.readline()
        if not line.startswith('$GP'):
            return
        if line.startswith('$GPVTG'):
            queue.put(':'.join((path, line)))


def writer(queue):
    """ Process to read from a queue.
    """
    while True:
        print queue.get()


def go():
    """ Multiplex GPS data.
    """
    queue = multiprocessing.Queue()

    multiprocessing.Process(target=writer, args=(queue,)).start()

    readers = {}

    while True:

        for (path, _, _) in serial.tools.list_ports.comports():

            if path not in readers.keys() or not readers[path].is_alive():

                readers[path] = multiprocessing.Process(
                    target=reader, args=(queue, path)
                )
                readers[path].start()


if __name__ == '__main__':
    go()
