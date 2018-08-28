import sys
sys.path.append('..')

import time

import ledwall.components as comp
from ledwall.geometry import (Point)

"""
Beispiel 1
==========



"""
s = comp.SerialSender(port_name='/dev/ttyACM0')

"""
Ab hier kannst du die Methoden der Klasse Display verwenden

"""

class Tutorial01(comp.SmileApplication):

    def __init__(self,sender, framerate):
        super().__init__(sender,framerate)
        self.form = Point(-2,0)

    def paint_form(self,dx,dy):
        self.form.x += dx
        self.form.y += dy
    
        self.display.set_pixel(self.form.x % 10,self.form.y % 10, (255,0,255))
        self.display.set_pixel((self.form.x+1) % 10,(self.form.y+1) % 10, (255,0,255))
        self.display.set_pixel(self.form.x % 10,(self.form.y+2) % 10, (255,0,255))
    
    def paint(self):
        self.display.fill((30,50,100))
        self.paint_form(1,1)
        

app = Tutorial01(s,5)
app.start_loop()

