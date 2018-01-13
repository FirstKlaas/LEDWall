from ..ledwall.components import *

d = Display(7,7, framerate=20)

color = HSVColor(0.,1.,1.)

while True:
	for i in range(360):
		color._h = i / 360.
		d.fill(color,True)

