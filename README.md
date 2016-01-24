# Motorsport development projects

Primary project is 'race-pi' for real-time telemetry for track driving.

This project is made up of a set of libraries for (currently):

    * Multiplexing multiple Serial streams (in my case, cheap GPS units).
    * Controlling an SPI LED display (in my case, this will show kph).

My hardware setup is utilises these libraries as shown in scripts/launch.py,
your setup will, no doubt, be different.

You can, of course, just use the libraries in any project :)

## Install

On Raspberry Pi:

    cd race-pi
    sudo python setup.py install

## Run

    cd race-pi
    python scripts/launch.py

## Other projects

There are other similar projects that I've done work on that lead to this one,
they've been bundled here for your information/entertainment.

### py-gps

An old project for rendering GPS location on Google Maps.

Formerly at https://github.com/thisismyrobot/py-gps

### gps-speedo

An old project for displaying speed on a voltmeter using GPS and a Picaxe.

Formerly at https://github.com/thisismyrobot/GPS-Speedo
