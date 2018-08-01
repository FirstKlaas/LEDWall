#!/usr/bin/env python3

from __future__ import print_function

import sys
sys.path.append('..')

from inputs import get_gamepad

from ledwall.components import *
from ledwall.games.tetris import Tetris

from ledwall.components.event import *

import time

from ledwall.util import TimeDelta

s = UDPSender(server='192.168.178.96')
#s = SerialSender()
d = Display(7, 7, s)
t = Tetris(d)

t.update()

def move_right():
    p = t.piece
    if t.testOverflowX(p, dx=1) == Tetris.VALID_POSITION:
        p['x'] += 1
        t.update()

def move_left():    
    p = t.piece
    if t.testOverflowX(p, dx=-1) == Tetris.VALID_POSITION:
        p['x'] -= 1
        t.update()

def move_up():
    p = t.piece
    if t.testOverflowY(p, dy=-1) == Tetris.VALID_POSITION:
        p['y'] -= 1
        t.update()

def new_piece(data):
    if data['state'] == 0: return

    if t.testOverflowX() != Tetris.VALID_POSITION:
        return

    if t.testOverflowY() != Tetris.VALID_POSITION:
        return

    if t.checkForCollision(t.piece) == Tetris.VALID_POSITION:
        t.writePieceToMatrix(t.piece)
        t.deleteCompleteRows()
        t.deleteCompleteColumns()
        t.new_piece()
        t.update()

def move_down():
    p = t.piece
    overflow = t.testOverflowY(p, dy=1)
    # When moving down, an overflow at the top is acceptable.
    # This is always true at the very beginning for every new piece,
    # because they start above the display.
    if overflow in [Tetris.VALID_POSITION, Tetris.OVERFLOW_TOP]:
        p['y'] += 1
        t.update()

def new_game(data):
    if data['state'] == 1:
        t.clearMatrix()
        t.new_piece()
        t.update()

def rotate_cw(data):
    if data['state'] == 1:
        t.rotateCW()
        t.update()

def rotate_ccw(data):
    if data['state'] == 1:
        t.rotateCCW()
        t.update()

def move_x(data):
    
    if data['state'] == 255:
        move_right()
    elif data['state'] == 0:
        move_left()
    
def move_y(data):
    if data['state'] == 255:
        move_down()
    elif data['state'] == 0:
        move_up()    

def update_display(data):
    d.update()    

actions = {
    (Event.SYSTEM,'update')      : update_display,
    (Event.GAMEPAD,'ABS_X')      : move_x,
    (Event.GAMEPAD,'ABS_Y')      : move_y,
    (Event.GAMEPAD,'BTN_PINKIE') : rotate_cw,
    (Event.GAMEPAD,'BTN_TOP2')   : rotate_ccw,
    (Event.GAMEPAD,'BTN_BASE4')  : new_game,
    (Event.GAMEPAD,'BTN_THUMB2') : new_piece,
}

running = True

try:
    events = EventDispatcher()
    events.add_emitter(FramerateEmitter(25))
    events.add_emitter(GamepadEmitter())

    while True:
        event = events.next_event()
        if event.type != Event.SYSTEM:
            #print(repr(event))
            pass

        action = actions.get((event.type,event.action),None)
        if action:
            action(event.data)

except KeyboardInterrupt:
    print("Good by")