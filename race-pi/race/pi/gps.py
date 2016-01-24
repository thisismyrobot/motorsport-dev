""" Multi-GPS multiplexer.
"""
import led
import multiprocessing
import serial.tools.list_ports


def reader(queue, path):
    """ Process to read from a comm port and put lines on a queue.
    """
    fails = 0

    # Connect at 9600 baud
    conn = serial.Serial(path, timeout=1)

    # Set 5Hz update rate
    conn.write(b'\xb5\x62\x06\x08\x06\x00\xc8\x00\x01\x00\x01\x00\xde\x6a')

    # Push data on to the queue.
    while fails < 10:
        # Check we have a GPS device
        line = conn.readline().strip()
        if not line.startswith('$GP'):
            fails += 1
            continue
        fails = 0
        queue.put(line)


def writer(queue):
    """ Process to read from a queue.
    """
    led_disp = led.LED()
    while True:
        line = queue.get()
        if line.startswith('$GPVTG'):
            kph = line.split(',')[7]
            if kph == '':
                led_disp.set('NO GPS')
            else:
                led_disp.set('{} kph'.format(kph))


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
