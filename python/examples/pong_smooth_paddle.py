#!/usr/bin/env python3

import sys
sys.path.append('..')

import math
import random

import ledwall.components as comp
import ledwall.components.event as event

# Gib hier den Port fuer den Arduino ein (siehe Arduino IDE)

s = comp.SerialSender(port_name='/dev/ttyACM0', baudrate=115200)

colors = {
    '0' : (255,255,0),
    '1' : (255,0,0),
    '2' : (0,255,255),
    'x' : (255,0,255),
    'o' : (0,0,0),
}

demo_block_A = [
    ".0.",
    "000",
]

demo_block_B = [
    "11.",
    ".11",
]

number_0 = [
    "111",
    "1.1",
    "1.1",
    "1.1",
    "111",
]

number_1 = [
    ".2.",
    ".2.",
    ".2.",
    ".2.",
    ".2.",
]

number_2 = [
    "222",
    "..2",
    "222",
    "2..",
    "222",
]

number_3 = [
    "222",
    "..2",
    "222",
    "..2",
    "222",
]

number_4 = [
    "2.2",
    "2.2",
    "222",
    "..2",
    "..2",
]

number_8 = [
    "222",
    "2.2",
    "222",
    "2.2",
    "222",
]

ghost = [
    ".xxx.",
    "xoxox",
    "xxxxx",
    "x.x.x",
]

number_sprites = [
    number_0,
    number_1,
    number_2,
    number_3,
    number_4,
    ghost,
    ghost,
    ghost,
    number_8,
    ghost,
]

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
        self.number_of_tries = 9

        """
        Hier ein Beispiel, wie auf Tasteneingaben reagiert werden kann.
        Zunaechst muss der KeyboardEmitter  angemeldet werden. Dadurch werden
        grundsaetzlich Tastatureingaben beruecksichtigt.

        Danach koennen Tastatureingaben an Methodenaufrufe gebunden werden.
        1 bedeutet 'Taste gedrueckt', 0 bedeutet 'Taste losgelasen'.
        """
        self.add_emitter(event.KeyboardEmitter())
        self.set_action(event.Event.KEYBOARD,'KEY_UP',1,self.btn_top_pressed)
        self.set_action(event.Event.KEYBOARD,'KEY_UP',0,self.btn_abs_y_released)
        self.set_action(event.Event.KEYBOARD,'KEY_DOWN',1,self.btn_down_pressed)
        self.set_action(event.Event.KEYBOARD,'KEY_DOWN',0,self.btn_abs_y_released)
        self.set_action(event.Event.KEYBOARD,'KEY_S',1,self.stop_loop)
        self.set_action(event.Event.KEYBOARD,'KEY_P',1,self.boo)

        #self.add_emitter(event.SerialEmitter())

        """
        Dies ist eine Beispielzeile, wie du weitere Aktionen registrieren kannst,
        wenn du z.B. einen anderen Controller verwendest.

        Du kannst dieselbe Methode auch mehreren Events zuordnen.
        """
        self.set_action(event.Event.GAMEPAD,'BTN_EAST',1,self.boo)


    def boo(self):
        """
        Mit get_pixel(x,y) kann man auch einen Farbwert auslesen.
        Man bekommt ein tuple mir den drei Werten fuer rot, gruen, blau
        geliefert. Dieses kann man auch bei set_pixel verwenden.
        """
        c = self.display.get_pixel(3,3)

    def draw_block(self,x,y,block,colors):
        for dy, row in enumerate(block):
            for dx, letter in enumerate(row):
                color = colors.get(letter,None)
                if color:
                    self.display.set_pixel(x+dx,y+dy,color)

    def draw_number(self, x,y, number):
        sprite = number_sprites[number]
        if sprite:
            self.draw_block(x,y,sprite,colors)

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
            self.ball_y = random.randrange(0,9,1)
            self.ball_dy = random.choice([-1,1])
            if self.number_of_tries > 0:
                self.number_of_tries -= 1
            else:
                self.number_of_tries = 9
        
    def paint(self):
        self.update_paddle_position()
        self.update_ballposition()
        self.draw_bg()
        #self.draw_block(0,0,demo_block_A,colors)
        #self.draw_block(1,4,demo_block_A,colors)
        #self.draw_block(5,6,demo_block_B,colors)
        self.draw_number(3,3,self.number_of_tries)
        self.draw_ball()
        self.draw_paddle()

        self.test_collision()

app = Pong(s,7)
app.start_loop()
