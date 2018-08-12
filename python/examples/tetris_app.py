#!/usr/bin/env python3

import sys
sys.path.append('..')

from ledwall.components import *
from ledwall.games.tetris import Tetris

from ledwall.components.event import *

import random

class FallingColumnAnimation(Animation):

    def __init__(self, column, color):
        super().__init__()
        self._column = column
        self._color = color
        self._tick = 0

    def animate(self):
        return (self._tick < self.rows)

    def paint(self, display):
        for y in range(self._tick, self.rows):
            display.set_pixel(self._column, y, self._color)
        self._tick += 1    

class DissolvingColumnAnimation(Animation):

    def __init__(self, column, duration=10, hue=0.0):
        super().__init__()
        self._column = column
        self._color = HSVColor(hue)
        self._tick = duration
        self._delta_value = 1.0 / duration 

    def animate(self):
        return (self._tick > 0)

    def paint(self, display):
        display.vertical_line(self._column, self._color)    
        self._color.value -= self._delta_value
        self._tick -= 1

class DissolvingRowAnimation(Animation):

    def __init__(self, row, duration=10, hue=0.0):
        super().__init__()
        self._row = row
        self._color = HSVColor(hue)
        self._tick = duration
        self._delta_value = 1.0 / duration 

    def animate(self):
        return (self._tick > 0)

    def paint(self, display):
        display.horizontal_line(self._row, self._color)    
        self._color.value -= self._delta_value
        self._tick -= 1

class TetrisGame(SmileApplication):

    MOVE_NOT   = 0
    MOVE_RIGHT = 1
    MOVE_LEFT  = 2
    MOVE_UP    = 3
    MOVE_DOWN  = 4

    def __init__(self,framerate=15):
        s = SerialSender(port_name='/dev/ttyACM0')
        #d = Display(10, 10, sender=s, mode=Display.MODE_ZIGZAG)

        super().__init__(s,framerate)

        self._board = Tetris(self.display)
        self.setup_game_controls()
        self.setup_xbox_controls()

        self.direction = TetrisGame.MOVE_NOT 
    
        self.move_actions = {
            TetrisGame.MOVE_RIGHT: self.move_right,
            TetrisGame.MOVE_LEFT: self.move_left, 
            TetrisGame.MOVE_UP: self.move_up,
            TetrisGame.MOVE_DOWN: self.move_down, 
        }
        self.colorize_blocks(HSVColor(0.3))

    def btn_select_pressed(self):
        self.animations += FallingColumnAnimation(self, 0, (255,0,255))

    def setup_game_controls(self):
        self.register_action(Event.GAMEPAD,'ABS_X',255 , self.right)
        self.register_action(Event.GAMEPAD,'ABS_X',127 , self.stop)
        self.register_action(Event.GAMEPAD,'ABS_X',0 , self.left)
        self.register_action(Event.GAMEPAD,'ABS_Y',255 , self.down)
        self.register_action(Event.GAMEPAD,'ABS_Y',127 , self.stop)
        self.register_action(Event.GAMEPAD,'ABS_Y',0 , self.up)
        self.register_action(Event.GAMEPAD,'BTN_PINKIE',1, self.rotate_cw)
        self.register_action(Event.GAMEPAD,'BTN_TOP2',1, self.rotate_ccw)
        self.register_action(Event.GAMEPAD,'BTN_BASE4',1, self.new_game)
        self.register_action(Event.GAMEPAD,'BTN_THUMB2',1, self.new_piece)

    def setup_xbox_controls(self):
        self.register_action(Event.GAMEPAD,'ABS_HAT0X',1 , self.right)
        self.register_action(Event.GAMEPAD,'ABS_HAT0X',0 , self.stop)
        self.register_action(Event.GAMEPAD,'ABS_HAT0X',-1 , self.left)
        self.register_action(Event.GAMEPAD,'ABS_HAT0Y',1 , self.down)
        self.register_action(Event.GAMEPAD,'ABS_HAT0Y',0 , self.stop)
        self.register_action(Event.GAMEPAD,'ABS_HAT0Y',-1 , self.up)
        self.register_action(Event.GAMEPAD,'BTN_TR',1, self.rotate_cw)
        self.register_action(Event.GAMEPAD,'BTN_TL',1, self.rotate_ccw)
        self.register_action(Event.GAMEPAD,'BTN_MODE',1, self.new_game)
        self.register_action(Event.GAMEPAD,'BTN_SOUTH',1, self.new_piece)
        self.register_action(Event.GAMEPAD,'BTN_EAST',1, self.colorize_blocks_random)

    def colorize_blocks_random(self):
        self.colorize_blocks(HSVColor(random.random()))

    def colorize_blocks(self, hsv):
        for id in self.board.block_ids:
            self.board.set_block_color(id, hsv)
            hsv.h += 0.15

    @property
    def piece(self):
        return self.board.piece
    
    @property
    def board(self):
        return self._board
    
    def right(self):
        self.direction = TetrisGame.MOVE_RIGHT

    def left(self):
        self.direction = TetrisGame.MOVE_LEFT

    def up(self):
        self.direction = TetrisGame.MOVE_UP

    def down(self):
        self.direction = TetrisGame.MOVE_DOWN

    def stop(self):
        self.direction = TetrisGame.MOVE_NOT 

    def make_move(self):
        action = self.move_actions.get(self.direction,None)
        if action: action()

    def move_right(self):
        p = self.piece
        if self.board.testOverflowX(p, dx=1) == Tetris.VALID_POSITION:
            p['x'] += 1

    def move_left(self):    
        p = self.piece
        if self.board.testOverflowX(p, dx=-1) == Tetris.VALID_POSITION:
            p['x'] -= 1

    def move_up(self):
        p = self.piece
        if self.board.testOverflowY(p, dy=-1) == Tetris.VALID_POSITION:
            p['y'] -= 1

    def new_piece(self):
        if self.board.testOverflowX() != Tetris.VALID_POSITION:
            return

        if self.board.testOverflowY() != Tetris.VALID_POSITION:
            return

        if self.board.checkForCollision(self.piece) == Tetris.VALID_POSITION:
            self.board.writePieceToMatrix(self.piece)
            for c in self.board.getCompletedColumns():
                self.board.deleteColumn(c)
                #self.animations += DissolvingColumnAnimation(self, c, hue=random.random())
                self.add_animation(FallingColumnAnimation(c, (255,255,255)))

            for c in self.board.getCompletedRows():
                self.board.deleteRow(c)
                self.add_animation(DissolvingRowAnimation(c, hue=random.random()))
            self.board.new_piece()
        
    def move_down(self):
        p = self.piece
        overflow = self.board.testOverflowY(p, dy=1)
        # When moving down, an overflow at the top is acceptable.
        # This is always true at the very beginning for every new piece,
        # because they start above the display.
        if overflow in [Tetris.VALID_POSITION, Tetris.OVERFLOW_TOP]:
            p['y'] += 1
            #self.board.update()

    def new_game(self):
        self.board.clearMatrix()
        self.board.new_piece()

    def rotate_cw(self):
        self.board.rotateCW()

    def rotate_ccw(self):
        self.board.rotateCCW()

    def paint(self):
        self.make_move()
        self.board.update()

if __name__ == "__main__":
    app = TetrisGame()
    app.start_loop()