#!/usr/bin/env python3

from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from ledwall.components import *

s = UDPSender(server='192.168.178.96')
d = Display(7,7,s)

h1 = HSVColor(1.0,1.0,1.0)

delta = 1.0 / len(d)

print("Anzahl der LEDs = {}".format(len(d)))

for i in range(49):
	h1.hue += delta
	d[i] = h1

d.update(True)


