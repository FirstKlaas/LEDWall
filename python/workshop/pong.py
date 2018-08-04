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
        self.ball_x = 1
        self.ball_y = 5
        self.ball_color = (200,200,255)
        self.ball_dx = 1
        self.ball_dy = 1
        #Schlaeger
        self.paddle_x = 9
        self.paddle_y = 5
        self.paddle_height = 3
        self.paddle_color = (200,255,10)
        self.paddle_dy = 0

    def draw_bg(self):
        self.display.fill(self.bg_color)

    def draw_ball(self):
        self.display.set_pixel(self.ball_x, self.ball_y, self.ball_color)

    def draw_paddle(self):
        for i in range(self.paddle_height):
            self.display.set_pixel(self.paddle_x, self.paddle_y+i, self.paddle_color) 

    def btn_abs_y_released(self):
        self.paddle_dy = 0

    def btn_down_pressed(self):
        self.paddle_dy = 1
        
    def update_paddle_position(self):
        y = self.paddle_y + self.paddle_dy
        
        if 0 <= y < 8:
            self.paddle_y = y
        
    def btn_top_pressed(self):
        self.paddle_dy = -1

    def btn_start_pressed(self):
        pass

    def test_collision(self):
        return self.ball_y in range(self.paddle_y,self.paddle_y+self.paddle_height) and self.paddle_x == self.ball_x+1
        

    def update_ballposition(self):
        new_x = self.ball_x + self.ball_dx
        new_y = self.ball_y + self.ball_dy
        if new_x < 0 :
            self.ball_dx *= -1
        elif self.test_collision():
            self.ball_dx *= -1
        if new_y < 0 :
            self.ball_dy *= -1
        elif new_y > 9 :
            self.ball_dy *= -1           
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x > 9:
            self.ball_x = 0
        
    def paint(self):
        self.update_paddle_position()
        self.update_ballposition()
        self.draw_bg()
        self.draw_ball()
        self.draw_paddle()
        self.test_collision()

app = Pong(s,7)
app.start_loop()
