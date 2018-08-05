#!/usr/bin/env python3

import sys
sys.path.append('..')

import math

import ledwall.components as comp
import ledwall.components.event as event

s = comp.SerialSender(port_name='/dev/ttyACM0')

class Pong(comp.SmileApplication):
    
    def __init__(self,sender,framerate):
        super().__init__(sender,framerate)
        #Hintergrundfarbe
        self.bg_color = (0,0,100)
        #Ball
   
        #Schlaeger


    def draw_bg(self):
        self.display.fill(self.bg_color)

    def draw_ball(self):
        pass

    def draw_paddle(self):
        pass 

    def btn_down_pressed(self):
        pass
        
    def btn_top_pressed(self):
        pass

    def btn_start_pressed(self):
        pass

    def test_collision(self):
        return 
        

    def update_ballposition(self):
        pass
        
    def paint(self):
        self.update_ballposition()
        self.draw_bg()
        self.draw_ball()
        self.draw_paddle()
        self.test_collision()

app = Pong(s,7)
app.start_loop()
