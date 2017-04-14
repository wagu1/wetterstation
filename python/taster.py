#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

# SET GPIO Button-Pin
BUTTON = 4  # Pin 7
LED    = 17  # Pin 11
led_on = False

def toggle_led():         
    global led_on
    led_on = not led_on
    GPIO.output(LED,GPIO.HIGH if led_on else GPIO.LOW)
    print "LED: ", led_on

# Main Function
def main():
    value = 0

    while True:

        if not GPIO.input(BUTTON):
            value += 0.01

        if value > 0:

            if GPIO.input(BUTTON):
                print "gedrueckt"
                toggle_led()
                main()

        time.sleep(0.03)
    return 0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUTTON, GPIO.IN)
    GPIO.setup(LED,GPIO.OUT)
    main()
