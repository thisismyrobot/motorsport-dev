""" Ultra-basic driver for the DFRobot 3-Wire LED Display.

    For Raspberry Pi.
"""
import spidev


# Based on:
#    http://www.dfrobot.com/wiki/index.php?title=SPI_LED_Module_(SKU:DFR0090)
FONT = {
    'a': 0xA0,
    'b': 0x83,
    'c': 0xa7,
    'd': 0xa1,
    'e': 0x86,
    'f': 0x8e,
    'g': 0xc2,
    'h': 0x8b,
    'i': 0xe6,
    'j': 0xe1,
    'k': 0x89,
    'l': 0xc7,
    'm': 0xaa,
    'n': 0xc8,
    'o': 0xa3,
    'p': 0x8c,
    'q': 0x98,
    'r': 0xce,
    's': 0x9b,
    't': 0x87,
    'u': 0xc1,
    'v': 0xe3,
    'w': 0xd5,
    'x': 0xb6,
    'y': 0x91,
    'z': 0xb8,
    '0': 0xc0,
    '1': 0xf9,
    '2': 0xa4,
    '3': 0xb0,
    '4': 0x99,
    '5': 0x92,
    '6': 0x82,
    '7': 0xf8,
    '8': 0x80,
    '9': 0x90,
    ' ': 0xff,
    '.': 0x7f,
}


class LED(object):
    """ LED display driver.
    """
    def __init__(self):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)

    def set(self, chars, clear=True):
        """ Set the display.
        """
        # Clear
        if clear:
            self._spi.xfer2([0xff]*8)

        out = []
        for c in chars:
            try:
                b = FONT[c.lower()]
            except KeyError:
                continue

            # Try to efficiently include the '.' using binary AND with
            # previous character.
            if c == '.':
                out[-1] = out[-1] & b
            else:
                out.append(b)

        self._spi.xfer2(out[::-1])


if __name__ == '__main__':
    led = LED()
    led.set('LED.01234')
