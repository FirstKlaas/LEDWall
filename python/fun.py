import json
import time
import pyowm
import random

from datetime import datetime

from ledwall.components import *
from ledwall.weather import *
from ledwall.util import *

def init_led_wall(settings):
	cfg = settings['led_wall']
	return Display(cfg["number_of_columns"],cfg["number_of_rows"], framerate=cfg["framerate"],baudrate=cfg["baudrate"])

def read_settings():
	with open('settings.json', 'r') as f:
		return json.load(f)

def update_temperature(weather, display, row=0):
	temp = weather.get_temperature('celsius')
	tempColor = (255,165,0) if temp > 0 else (0,0,80)	
	itemp = abs(int(temp['temp']))
	display.writeBitmask(row,itemp,tempColor,(5,5,5))

def update_time(display, row=4):
	t = datetime.now();
	d.writeBitmask(row,t.hour, (128,0,128),(5,0,5))
	d.writeBitmask(row+1,t.minute, (0,128,128),(0,5,5))
	d.writeBitmask(row+2,t.second, (0,128,0),(0,5,0))

settings = read_settings()
d        = init_led_wall(settings)
weather  = Weather(settings)

def run():
	while True:
		update_temperature(weather.weather,d)
		i = 0
		while i < 60*10:
			update_time(d)
			d.update()
			time.sleep(1)
			i += 1

if __name__ == '__main__':
		run()