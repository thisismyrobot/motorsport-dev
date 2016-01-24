""" Main process manager for Race Pi.
"""
import race.pi.gps
import race.pi.led


def launch():
    led = race.pi.led.LED()
    led.set('No GPS')
    race.pi.gps.go()
