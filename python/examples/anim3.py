#!/usr/bin/env python3

from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from random import randint

import ledwall.components as comp

s = comp.TCPSender( server='172.16.8.70' )
d = comp.Display(7,7,s, framerate=20)

color = comp.HSVColor()
color.value = 0.5

while True:
	for x in range(7):
		for y in range(7):
			d.set_pixel(x,y,color,True)
	color.hue += 0.3		