import RPi.GPIO as GPIO

BUTTON =  4  # GPIO4 = Pin 7
LED    = 17  # GPIO17 = Pin 11

led_on = False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

def toggle_led(channel):         
    global led_on
    led_on = not led_on
    GPIO.output(LED,GPIO.HIGH if led_on else GPIO.LOW)
    print "LED: ", led_on

GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=toggle_led, bouncetime=200)     

try:
    while True:
        pass

except KeyboardInterrupt:
    print "Ctrl-C - quit"

finally:
    GPIO.cleanup() 
