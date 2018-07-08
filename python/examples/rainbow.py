import sys
sys.path.append('..')

from ledwall.components import *

s = SerialSender(baudrate=500000)

d = Display(7, 7, s)

hsv = HSVColor(0.0, 1.0, 1.0)

while True:
    d.fill(Color.convert(hsv), True)
    hsv._h += 0.01
