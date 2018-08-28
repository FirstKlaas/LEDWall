#!/usr/bin/env python3

import sys
sys.path.append('..')

import ledwall.components as comp

s = comp.UDPSender( server='LEDPanel-ONE')
d = comp.Display(7,7,s,framerate=10)

d.show_image('../sprites/monster.png')
while True:
    d.update()
    d.shift_right()

