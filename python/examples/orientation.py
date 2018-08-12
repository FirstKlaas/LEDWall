import sys
sys.path.append('..')

import time

import ledwall.components as comp
from ledwall.geometry import *

"""
Orientation
===========

Diese Script macht nichts weiter, als einen farbigen
Pixel in die obere linke Ecke des LED Panels zu zeichnen.

Damit kann das LED Panel leicht ausgerichtet werden.
"""
s = comp.SerialSender(port_name='/dev/ttyACM0')


class Orientation(comp.SmileApplication):

    def __init__(self,sender, framerate):
        super().__init__(sender,framerate)



    def paint(self):
        self.display.set_pixel(0,0,(30,50,100))
        

app = Orientation(s,1)
app.start_loop()

