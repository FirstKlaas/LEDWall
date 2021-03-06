#!/usr/bin/env python3

import sys
sys.path.append('..')

import random
import ledwall.components as comp

s1 = comp.UDPSender( server='LEDPanel-ONE')
s2 = comp.UDPSender( server='LEDPanel-TWO')

r1 = comp.RegionSender(0,2,7,7,s1, mode=comp.WireMode.LTR)
r2 = comp.RegionSender(7,0,10,10,s2,mode=comp.WireMode.ZIGZAG)

senders = comp.ListSender([r1,r2], add_async=True)
d = comp.Display(17,10,senders,framerate=20, async=False)

d.show_image('../sprites/arrow_right_1710.png')
#d.show_image('../sprites/LEDWALL-FONT.png')

def fill_column():
    for y in range(d.rows):
        d.set_pixel(0,y,(comp.HSVColor(random.random(),1.0,1.0)))

while True:
    d.update()
    d.shift_right()
    #fill_column()

