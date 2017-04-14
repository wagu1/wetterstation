#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
from BMP280 import BMP280
import time
import subprocess
import Adafruit_GPIO.I2C as I2C

# für Taster
import RPi.GPIO as GPIO
#BUTTON =  4  # GPIO4 = Pin 7
BUTTON =  8  # GPIO4 = Pin 24

font = ImageFont.load_default()
#device = ssd1306(port=1, address=0x3C)
device = sh1106(port=1, address=0x3C)

bmp280 = BMP280(I2C,0x77)

#print ("T :{:.2f} C".format(bmp280.getTemperature()))
#print ("p :{:.2f} hPa".format(bmp280.getPressure()))
#print ("h :{:.2f} m".format(bmp280.getAltitude()))

# -----------------------------------------------------------------
# Aktuelle Sensor-Temperatur auslesen
# -----------------------------------------------------------------
def get_bmp280_temp():
    return 'T = {:6.2f} C'.format(bmp280.getTemperature())

# -----------------------------------------------------------------
# Aktuelle Sensor-Druck auslesen
# -----------------------------------------------------------------
def get_bmp280_pressure():
    return 'T = {:6.1f} hPa'.format(bmp280.getPressure())

# -----------------------------------------------------------------
# Aktuelle Sensor-Höhe auslesen
# -----------------------------------------------------------------
def get_bmp280_altitude():
    return 'T = {:6.1f} m'.format(bmp280.getAltitude())


# -----------------------------------------------------------------
# Aktuelle CPU-Temperatur auslesen
# -----------------------------------------------------------------
def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    t = float(cpu_temp)/1000
    return "CPU-Temp:  " + str(round(t, 2)) + "°C"

# -----------------------------------------------------------------
# liefert die Geschwindigkeit der CPU in MHz als String
# -----------------------------------------------------------------
def get_cpu_speed():
    tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    cpu_speed = tempFile.read()
    tempFile.close()
    s = float(cpu_speed)/1000
    return "CPU-Speed: " + str(round(s, 0)) + "MHz"

# -----------------------------------------------------------------
# liefert das aktuelle Datum
# -----------------------------------------------------------------
def get_time():
    return time.strftime("%a %d %b %H:%M")
    
# -----------------------------------------------------------------
# liefert die aktuelle IP4-Adresse
# -----------------------------------------------------------------
def get_IP4():
    return "IP:  " + subprocess.check_output(["hostname","-I"])[:-2]


# -----------------------------------------------------------------
# Aktuelle Werte des Raspi anzeigen
# -----------------------------------------------------------------
def show():
    with canvas(device) as draw:
        # Draw a rectangle of the same size of screen
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=0)

        # Load fonts
        font = ImageFont.load_default()
        font1 = ImageFont.truetype('redalert.ttf', 12)

        # Write four lines of text.
        x   = 2
        top = 2
        dy = 12
        draw.text((x, top),    'Welcome to RPI !',  font=font,  fill=255)
        draw.text((x, top+1*dy), get_time() ,       font=font1, fill=255)
        draw.text((x, top+2*dy), get_IP4() ,        font=font1, fill=127)
        draw.text((x, top+3*dy), get_cpu_temp()  ,  font=font1, fill=255)
        #draw.text((x, top+3*dy), readTemp() ,       font=font1, fill=255)
        draw.text((x, top+4*dy), get_cpu_speed()  , font=font1, fill=255)

# -----------------------------------------------------------------
# Aktuelle Werte des Sensors BMP280 anzeigen
# -----------------------------------------------------------------
def showBMP280():
    with canvas(device) as draw:
        # Draw a rectangle of the same size of screen
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=0)

        # Load fonts
        font = ImageFont.load_default()
        font1 = ImageFont.truetype('redalert.ttf', 12)

        # Write four lines of text.
        x   = 2
        top = 2
        dy = 12
        draw.text((x, top),    'Drucksensor BMP280 !',    font=font,  fill=255)
        draw.text((x, top+2*dy), get_bmp280_temp() ,      font=font1, fill=255)
        draw.text((x, top+3*dy), get_bmp280_pressure() ,  font=font1, fill=127)
        draw.text((x, top+4*dy), get_bmp280_altitude() ,  font=font1, fill=255)

# -----------------------------------------------------------------
# Begrüßungsbildschirm anzeigen
# -----------------------------------------------------------------
def greeting():
    with canvas(device) as draw:
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=0)

        # Load default font.
        font = ImageFont.load_default()
        font1 = ImageFont.truetype('redalert.ttf', 12)

        x   = 2
        top = 2
        dy = 12
        draw.text((x, top),    'Welcome to RPI !',  font=font,  fill=255)
        draw.text((x, top+2*dy), 'Wetterstation HOME' , font=font1, fill=255)
        
# -----------------------------------------------------------------
# Daten für 5s anzeigen, danach Bildschirm löschen
# -----------------------------------------------------------------
def showValue(channel):         
    print ("Taster gedrückt")
    show()
    time.sleep(3)
    showBMP280()
    time.sleep(3)
    clearScreen()

# -----------------------------------------------------------------
# Bildschirm löschen
# -----------------------------------------------------------------
def clearScreen():
    with canvas(device) as draw:
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=0, fill=0)
    

# -----------------------------------------------------------------
# Beginn des Hauptprogramms
# -----------------------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=showValue, bouncetime=20)     

greeting()

try:
    while True:
        pass

except KeyboardInterrupt:
    print ("Ctrl-C - quit")

finally:
    GPIO.cleanup() 



