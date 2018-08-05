import sys
sys.path.append('..')

import time

import ledwall.components as comp


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
        self.x = 0
        self.y = 8
        self.dx = 1
        self.color = (255,0,0)


    def linie(self):
        for i in range(1,9):
            self.display.set_pixel(i, 6, (0,0,255))

    def move(self):
        self.display.set_pixel(self.x,self.y, (0,0,0))
        self.x += self.dx
        self.display.set_pixel(self.x,self.y, (0,255,0))
        if self.x == 9:
            self.dx = -1
        elif self.x == 0:
            self.dx = 1
            

    def paint(self):
        self.display.set_pixel(0, 0, self.color)
        self.linie()
        self.move()
        

app = Tutorial01(s,2)
app.start_loop()

