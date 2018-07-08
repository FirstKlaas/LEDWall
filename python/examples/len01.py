from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from random import randint

from ledwall.components import *

d = Display(7,7,UDPSender(server='192.168.178.96'),framerate=10)


while True:
	color   = Color(randint(0,255),randint(0,255),randint(0,255))
	d.fill(color)
	for i in range(11):
		white = Color(randint(0,255),randint(0,255),randint(0,255))
		d.set_pixel(randint(0,6), randint(0,6), white)
	d.update()