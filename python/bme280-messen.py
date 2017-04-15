#!/usr/bin/python 
# -*- coding: utf-8 -*-

from Adafruit_BME280 import *
import urllib

sensor = BME280(mode=BME280_OSAMPLE_8)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

url = "http://<server>/upload.php?m=outdoor&t=" +str(round(degrees, 2)) + "&p=" +str(round(hectopascals, 2)) + "&f=" + str(round(humidity, 2))

urllib.urlopen(url)

print ("Temperatur (in C)   = {0:0.3f} C".format(degrees))
print ("Luftdruck (in hPa)  = {0:0.2f} hPa".format(hectopascals))
print ("Luftfeuchtigkeit    = {0:0.2f} %".format(humidity))

