import sys
sys.path.append('..')

from ledwall.components import *
from ledwall.geometry import *

"""
Beispiel 1
==========



"""
s = SerialSender(port_name='/dev/ttyACM0')
d = Display(10,10,s, mode=Display.MODE_ZIGZAG, framerate=10)

print("Anzahl der LEDs = {}".format(len(d)))

"""
Ab hier kannst du die Methoden der Klasse Display verwenden

"""

block = Rectangle(9,5,3,3)
form = Point(-2,3)

def paint_form(dx,dy):
    form.x += dx
    form.y += dy
    
    d.set_pixel(form.x,form.y, (255,0,255))
    d.set_pixel(form.x+1,form.y+1, (255,0,255))
    d.set_pixel(form.x,form.y+2, (255,0,255))
    
def move(dx,dy):
    block.x += dx
    block.y += dy
    d.fill_rect(block.x,block.y,block.width,block.height,(120,120,255))

hsv = HSVColor(0,1.0,1.0)


"""
for x in range(10):
    for y in range(10):
        d.set_pixel(x,y,hsv)
        hsv.hue += 0.1

hsv.hue = 0.5
d.horizontal_line(1, hsv)
d.vertical_line(1, hsv)
d.fill_rect(3,3,5,4,(255,255,255))
d.set_pixel(2,6, (255,0,0))
d.set_pixel(0,9, (255,0,255))
d.set_pixel(3,7, (255,0,255))
"""

"""
Nun aktualisiere das LED Display.

"""
d.update()

for i in range(10):
    d.fill((30,50,100))
    #move(-1,0)
    paint_form(1,1)
    #d.set_pixel(5,i,(200,200,200))
    d.update()


