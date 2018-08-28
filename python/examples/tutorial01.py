import sys
sys.path.append('..')

import time

import ledwall.components as comp
from ledwall.geometry import (Point, Rectangle)

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
        self.block = Rectangle(9,5,3,3)
        self.form = Point(-2,0)
        self.hsv = comp.HSVColor(0,1.0,1.0)

    def paint_form(self,dx,dy):
        self.form.x += dx
        self.form.y += dy
    
        self.display.set_pixel(self.form.x % 10,self.form.y % 10, (255,0,255))
        self.display.set_pixel((self.form.x+1) % 10,(self.form.y+1) % 10, (255,0,255))
        self.display.set_pixel(self.form.x % 10,(self.form.y+2) % 10, (255,0,255))
    
    def move(self,dx,dy):
        self.block.x += dx
        self.block.y += dy
        
        self.display.fill_rect(self.block.x,self.block.y,self.block.width,self.block.height,(120,120,255))


    def paint(self):
        self.display.fill((30,50,100))
        self.paint_form(1,1)
        

app = Tutorial01(s,10)
app.start_loop()

