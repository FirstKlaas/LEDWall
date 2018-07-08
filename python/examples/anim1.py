from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from random import randint

from ledwall.components import *

d = Display(7,7,UDPSender(server='192.168.178.96'),framerate=20)


def runforever(display, props):
	return True

def coloured_rain(display, deltaHue = 0.01, runfunc=runforever, props={}):
	color = HSVColor(0.0,1.0,1.0)
	display.fill(color,True)
	m = 3
	d = {}
	d.update(props)
	while runfunc(display, d):
		display.move(m)
		display[0] = Color.fromHSVColor(color)
		color.hue += deltaHue
		display.update()
		m = ((m+1) % display.columns) + 1


def glitter(display, count, runfunc=runforever, props={}):
	hue = 0.0
	val_delta = 0.01
	hue_delta = 0.003

	def random_value():
		return  randint(40,100) / 100.

	def random_saturation():
		return  randint(60,100) / 100.

	def random_pixel():
		return { "x" : randint(0,display.columns-1), "y" : randint(0,display.columns-1), "color" : HSVColor(hue,random_saturation(),random_value())}	

	glitter_pixels = [random_pixel() for x in range(count) ] 
	
	def update_glitter():
		for i,p in enumerate(glitter_pixels):
			col = p['color']
			col.hue = hue
			if col.value > val_delta:
				col.value -= val_delta
			else:
				glitter_pixels[i] = random_pixel()			

	def draw():
		for p in glitter_pixels:
			d.set_pixel(p['x'], p['y'], p['color'])
		d.update()

	while runfunc(display, props):
		draw()
		hue += hue_delta
		update_glitter();

def run_ntimes_function(display, d):
	if not "counter" in d:
		d["counter"] = 1000
	if d["counter"] == 0: 
		return False
	d["counter"] -= 1
	return True

#coloured_rain(d, runfunc=run_ntimes_function)
#coloured_rain(d)
glitter(d, 20)