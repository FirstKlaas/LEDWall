import json
import time
import pyowm
import random

from ledwall.components import *
from ledwall.weather import *
from ledwall.util import *
from ledwall.widgets.clocks import BinaryCodedSexagesimalClock as BCD

def init_led_wall(settings):
	cfg = settings['led_wall']
	return Display(cfg["number_of_columns"],cfg["number_of_rows"], framerate=cfg["framerate"] or 15,baudrate=cfg["baudrate"] or 1000000)

def update_temperature(weather, display, row=0):
	temp = weather.get_temperature('celsius')
	tempVal = int(temp['temp'])
	tempColor = (255,165,0) if tempVal > 0 else (0,0,80)	
	itemp = abs(tempVal)
	display.writeBitmask(row,itemp,tempColor,(5,5,5))

settings    = Settings()
d           = init_led_wall(settings)
weather     = Weather(settings)
bcd         = BCD(0,4)
bcd.display = d

def run():
	while True:
		update_temperature(weather.weather,d)
		i = 0
		while i < 60*10:
			bcd.update(True)
			time.sleep(1)
			i += 1

if __name__ == '__main__':
		run()