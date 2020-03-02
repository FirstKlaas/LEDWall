import sys
sys.path.append('..')

import random
from ledwall.components import (HSVColor, Display, Color, SerialSender)

s = SerialSender(port_name="/dev/ttyUSB0", baudrate=115400)

d = Display(7, 7, s, framerate=60)

hsv = HSVColor(0.0, 1.0, 1.0)

class AnimOne:

    def __init__(self):
        self.create_pixel()
        self.frame = 0

    def create_pixel(self):
        self.pixels = [[random.random(), random.randint(0,7), random.randint(0,7)] for x in range(20)]

    def update_hue(self):
        for pixel in self.pixels:
            pixel[0] += 0.0001
            if pixel[0] > 1.0:
                pixel[0] = 0.0

    def paint(self, display: Display, bg_hue:float):
        for pixel in self.pixels:
            display.set_pixel(pixel[1], pixel[2], HSVColor(pixel[0], 1.0, 1.0))
            self.update_hue()
        self.frame += 1
        if self.frame == 200:
            self.create_pixel()
            self.frame = 0

class AnimTwo:

    def __init__(self):
        self.create_pixel()
        self.frame = 0

    def create_pixel(self):
        self.pixels = [[random.random(), random.randint(0,7), random.randint(0,7)] for x in range(20)]

    def update_hue(self):
        for pixel in self.pixels:
            pixel[0] += 0.0001
            if pixel[0] > 1.0:
                pixel[0] = 0.0

    def paint(self, display: Display, bg_hue:float):
        for pixel in self.pixels:
            display.set_pixel(pixel[1], pixel[2], HSVColor(pixel[0], 1.0, 1.0))
            pixel[0] += 0.002
            if pixel[0] > 1.0:
                pixel[0] = 0.0

            if abs(pixel[0] - bg_hue) < 0.01:
                pixel[0] = bg_hue + 0.03
                pixel[1] = random.randint(0,7)
                pixel[2] = random.randint(0,7)


        self.frame += 1


class AnimArrow:

    def __init__(self):
        self.display = Display(7,7)
        self.display.fill(HSVColor(0.7,1.0,0.4))


    def paint(self, display: Display, bg_hue:float):
        display.copy_region_from(self.display)


animation = AnimTwo()

while True:
    d.fill(Color.convert(hsv))
    animation.paint(d, hsv.hue)
    d.update()
    hsv.h += 0.001
