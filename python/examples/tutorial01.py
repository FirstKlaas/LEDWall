#!/usr/bin/env python3

import sys
sys.path.append('..')

from ledwall.components import *

#s = UDPSender(server='192.168.178.96')
s = SerialSender(port_name='/dev/ttyACM1')
d = Display(10,10,s,framerate=5)

print("Anzahl der LEDs = {}".format(len(d)))

d.set_pixel(2,6, (255,0,0))
d.set_pixel(0,9, (255,0,255))
d.set_pixel(3,7, (255,0,255))

d.update()


