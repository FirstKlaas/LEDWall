#!/usr/bin/env python3

import sys
sys.path.append('..')

from ledwall.components import *
from ledwall.components.event import *
import ledwall.geometry as geo

import random

class SequenceAnimation():

    def __init__(self, sequence, frames_per_color=10):
        self._color = None
        self.fpc = frames_per_color
        self._sequence = self.generate_frames_sequence(sequence, self.fpc)

    @property
    def frames_per_color(self):
        return self._frames
    
    def generate_frames_sequence(self, seq, fpc):
        l = [None]*20
        for c in seq:
            l+= [c]*fpc + [None]*fpc
        return l

    def __iter__(self):
        return iter(self._sequence)
        
class SensoGame(SmileApplication):

    def __init__(self,framerate=15):
        s = SerialSender(port_name='/dev/ttyACM0')
        
        super().__init__(s,framerate)
        self._red    = {
            'rect'  : (5,1,4,4),
            'color' : HSVColor(0.0),
        }

        self._green    = {
            'rect'  : (5,5,4,4),
            'color' : HSVColor(0.3),
        }

        self._orange    = {
            'rect'  : (1,1,4,4),
            'color' : HSVColor(0.15),
        }

        self._blue = {
            'rect'  : (1,5,4,4),
            'color' : HSVColor(0.6),
        }


        self._fields = { 
            'r' : self._red,
            'g' : self._green,
            'o' : self._orange,
            'b' : self._blue,
        }
        
        self._on  = 1.0
        self._off = 0.7

        self.switch_off()

        self.register_action(Event.GAMEPAD,'BTN_MODE',1, self.new_game_pressed)
        self.register_action(Event.GAMEPAD,'BTN_MODE',0, self.new_game_released)

        self.play_buttons_actionmap = [
            (Event.GAMEPAD,'BTN_SOUTH',1, self.field_green_pressed),
            (Event.GAMEPAD,'BTN_SOUTH',0, self.field_green_released),
            (Event.GAMEPAD,'BTN_EAST',1, self.field_red_pressed),
            (Event.GAMEPAD,'BTN_EAST',0, self.field_red_released),
            (Event.GAMEPAD,'BTN_NORTH',1, self.field_blue_pressed),
            (Event.GAMEPAD,'BTN_NORTH',0, self.field_blue_released),
            (Event.GAMEPAD,'BTN_WEST',1, self.field_orange_pressed),
            (Event.GAMEPAD,'BTN_WEST',0, self.field_orange_released),
        ]

        self._sequence = []
        self._bullets = self.build_bullet_list()

        self._play_index = None
        self.register_play_buttons()
        self.paint_fields()

    def __getitem__(self, index):
        return self._fields[index]

    def build_bullet_list(self):
        l = [(x,0) for x in range(10)]
        l += [(9,y) for y in range(1,10)]
        return l

    def new_game_pressed(self):
        self.display.fill((100,255,100))
        self.switch_off()
        self.paint_fields()
        self.clear_play_buttons()
        self.paint_function = None
        self._sequence = []
        self._play_index = 0

    def paint_bullets(self, hitindex=0):
        for i in range(len(self._sequence)):
            self.display.set_pixel(*self._bullets[i], (0,100,0) if i < hitindex else (200,200,200))       

    def new_game_released(self):
        self.display.fill((0,0,0))
        self.add_sequence_item()
        self.paint_challenge(self.paint_bullets)
        
    def add_sequence_item(self):
        self._sequence.append(random.choice(list(self._fields.keys())))

    def register_play_buttons(self):
        for action in self.play_buttons_actionmap:
            self.register_action(*action)

    def clear_play_buttons(self):
        for action in self.play_buttons_actionmap:
            self.unregister_action(*action[:3])

    def test_user_decision(self, color):
        self.clear_play_buttons()
        #print("Index: {} color = {} sequence = {}".format(self._play_index, color, self._sequence))
        if self._sequence[self._play_index] == color:
            self._play_index += 1
            self.paint_bullets(self._play_index)
            if self._play_index == len(self._sequence):
                self._play_index = 0
                self.add_sequence_item()
                self.paint_challenge(self.paint_bullets)
            else:
                self.register_play_buttons()
        else:
            self.game_over()
            #new_game()

    def field_red_pressed(self):
        self.switch_on(self._red)
        
    def field_red_released(self):
        self.switch_off(self._red)
        self.test_user_decision('r')

    def field_orange_pressed(self):
        self.switch_on(self._orange)

    def field_orange_released(self):
        self.switch_off(self._orange)
        self.test_user_decision('o')

    def field_blue_pressed(self):
        self.switch_on(self._blue)

    def field_blue_released(self):
        self.switch_off(self._blue)
        self.test_user_decision('b')

    def field_green_pressed(self):
        self.switch_on(self._green)
        
    def field_green_released(self):
        self.switch_off(self._green)
        self.test_user_decision('g')

    def hello(self):
        pass

    def switch_off(self, field=None):
        if field:
            field['color'].value = self._off
        else:
            for f in self._fields.values():
                f['color'].value = self._off

    def switch_on(self, field=None):
        if field:
            field['color'].v = self._on
        else:
            for f in self._fields.values():
                f['color'].value = self._on

    def paint_fields(self):
        for f in self._fields.values():
            self.display.fill_rect(*f['rect'],f['color'])

    def game_over(self, clb=None):
        self.clear_play_buttons()

        red = HSVColor(0)
        self.switch_off()

        def paint():
            self.display.fill(red)
            self.paint_fields()
            red.v -= 0.05
            if (red.v < 0.06):
                self.paint_function = self.paint_fields

        self.paint_function = paint

    def paint_challenge(self, clb=None):
        i = iter(SequenceAnimation(self._sequence,5))

        def paint():
            self.clear_play_buttons()
            try:
                c = next(i)
                self.switch_off()
                if c:
                    self.switch_on(self._fields[c])
                self.paint_fields()
         
            except StopIteration:
                self.register_play_buttons()
                self.paint_function = self.paint_fields
                if clb: clb()

        self.paint_function = paint


if __name__ == '__main__':
    app = SensoGame()
    app.start_loop()
