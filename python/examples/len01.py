from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from random import randint

from ledwall.components import *

#s = UDPSender(server='192.168.178.96')
s = SerialSender(port_name='/dev/ttyACM0')

d = Display(10,10,s,framerate=10)


while True:
	color   = Color(randint(0,255),randint(0,255),randint(0,255))
	d.fill(color)
	for i in range(11):
		white = Color(randint(0,255),randint(0,255),randint(0,255))
		d.set_pixel(randint(0,d.columns), randint(0,d.rows), white)
	d.update()