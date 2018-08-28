#!/usr/bin/env python3

from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

from random import randint

import ledwall.components as comp

d = comp.Display(10,10,comp.SerialSender(port_name='/dev/ttyACM0'), framerate=15)

class GlitterApp(comp.Application):

    def __init__(self,count):
        super().__init__(d,10)
        self.hue = 0.0
        self.val_delta = 0.01
        self.hue_delta = 0.003
        self.glitter_pixels = [self.random_pixel() for x in range(count) ] 

            
    def paint(self):
        self.update_glitter()
        for p in self.glitter_pixels:
            self.display.set_pixel(p['x'], p['y'], p['color'])                

    def random_value(self):
        return  randint(40,100) / 100.

    def random_saturation(self):
        return  randint(60,100) / 100.

    def random_pixel(self):
        x = randint(0,self.display.columns-1)
        y = randint(0,self.display.rows-1)
        color = comp.HSVColor(self.hue,self.random_saturation(),self.random_value())
        return { "x" : x, "y" : y, "color" : color}    
    
    def update_glitter(self):
        for i,p in enumerate(self.glitter_pixels):
            col = p['color']
            col.hue = self.hue
            if col.value > self.val_delta:
                col.value -= self.val_delta
            else:
                self.glitter_pixels[i] = self.random_pixel()          

app = GlitterApp(60)
app.start_loop()
