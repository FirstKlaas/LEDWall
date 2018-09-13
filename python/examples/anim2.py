#!/usr/bin/env python3

import sys
sys.path.append('..')

from random import randint
import cProfile
import ledwall.components as comp

#d = comp.Display(10,10,comp.SerialSender(port_name='/dev/ttyACM0'), framerate=15)

s1 = comp.UDPSender( server='LEDPanel-ONE')
s2 = comp.UDPSender( server='LEDPanel-TWO')

r1 = comp.RegionSender(0,2,7,7,s1, mode=comp.WireMode.LTR)
r2 = comp.RegionSender(7,0,10,10,s2,mode=comp.WireMode.ZIGZAG)

senders = comp.ListSender([r1,r2], add_async=True)
d = comp.Display(17,10,senders)

class GlitterApp(comp.Application):

    def __init__(self,count):
        super().__init__(d,10)
        self.hue = 0.0
        self.val_delta = 0.01
        self.hue_delta = 0.001
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
                self.hue += self.hue_delta          

app = GlitterApp(60)
#cProfile.run('app.start_loop()','stats.txt')
app.start_loop()