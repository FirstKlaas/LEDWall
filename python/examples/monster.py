#!/usr/bin/env python3

import sys
sys.path.append('..')

import random
import ledwall.components as comp

s = comp.UDPSender( server='LEDPanel-ONE')
r = comp.RegionSender(3,2,7,7,s)
d = comp.Display(14,14,r,framerate=1, async=False)

#d.show_image('../sprites/arrow_right.png')
r.x += 3

d.fill((255,0,0))
d.fill_rect(7,0,7,7,(0,255,0))
d.fill_rect(0,7,7,7,(0,0,255))
d.fill_rect(7,7,7,7,(255,0,255))

def fill_column():
    for y in range(d.rows):
        d.set_pixel(0,y,(comp.HSVColor(random.random(),1.0,1.0)))

while True:
    d.update()
    #d.shift_right()
    #fill_column()

