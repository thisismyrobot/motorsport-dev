# Motosport development projects

Primary project is 'race-pi' for real-time telemetry for track driving.

## NOTE

This all requires a fairly specific hardware setup that I haven't yet
documented...

## Install

On Raspberry Pi:

    cd race-pi
    sudo python setup.py install

## Run

This launch.py script coordinates the different modules etc. This is what
you'd no-doubt change the most for your hardware setup.

    cd race-pi
    python scripts/launch.py

## py-gps

An old project for rendering GPS location on Google Maps.

Formerly at https://github.com/thisismyrobot/py-gps

## gps-speedo

An old project for displaying speed on a voltmeter using GPS and a Picaxe.

Formerly at https://github.com/thisismyrobot/GPS-Speedo
