import sys
sys.path.append('..')

from ledwall.components import *

#s = UDPSender(server='192.168.178.96')
s = SerialSender(port_name='/dev/ttyACM0')

d = Display(10,10,s, framerate=30)

color = HSVColor(0.,1.,1.)

while True:
	for i in range(360):
		color._h = i / 360.
		d.fill(color,True)

