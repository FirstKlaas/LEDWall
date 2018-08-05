#!/usr/bin/env python3

import sys
sys.path.append('..')

import ledwall.components as comp
import ledwall.components.event as event

#gebe hier den Port fuer den Arduino ein (siehe Arduino IDE)
s = comp.SerialSender(port_name='/dev/ttyACM0')

class MyApp(comp.SmileApplication):
    
    def __init__(self,sender,framerate):
        super().__init__(sender,framerate)
        self.x = 5
        self.y = 5
        self.color  = (255,0,0)

    def btn_left_pressed(self):
        print('Nach links')
        if self.x > 0:
            self.x -= 1 
        
    def btn_right_pressed(self):
        print('Nach rechts')
        pass

    def btn_top_pressed(self):
        print('Nach oben')
        pass
        
    def btn_down_pressed(self):
        print('Nach unten')
        pass

    def btn_a_pressed(self):
        print('A pressed')
        pass
        
    def btn_b_pressed(self):
        print('B pressed')
        pass
        
    def btn_r_pressed(self):
        print('R pressed')
        pass
        
    def btn_l_pressed(self):
        print('L pressed')
        pass

    def btn_x_pressed(self):
        print('X pressed')
        pass

    def btn_y_pressed(self):
        print('Y pressed')
        pass

    def btn_select_pressed(self):
        print('SELECT pressed')
        pass
        
    def btn_start_pressed(self):
        print('START pressed')
        pass
        
    def paint(self):
        self.display.set_pixel(self.x, self.y, self.color)

app = MyApp(s,20)
app.start_loop()
