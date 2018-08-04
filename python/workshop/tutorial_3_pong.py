#!/usr/bin/env python3

import sys
sys.path.append('..')

import math

import ledwall.components as comp
import ledwall.components.event as event

#gebe hier den Port fuer den Arduino ein (siehe Arduino IDE)

s = comp.SerialSender(port_name='/dev/ttyACM1')

class Pong(comp.SmileApplication):
    
    def __init__(self,sender,framerate):
        super().__init__(sender,framerate)
        #Hintergrundfarbe
        self.bg_color = (0,0,155)
        #Ball

        #Schlaeger


    def draw_bg(self):
        pass
        

    def draw_ball(self):
        pass

    def draw_paddle(self):
        pass

    """
    def btn_abs_y_released(self):
        pass



    def btn_down_pressed(self):
        pass
        
    def update_paddle_position(self):
        pass
        
    def btn_top_pressed(self):
"""

    def btn_start_pressed(self):
        pass

    def test_collision(self):
        return
        

    def update_ballposition(self):
        pass

        
    def paint(self):
        pass


app = Pong(s,7)
app.start_loop()
