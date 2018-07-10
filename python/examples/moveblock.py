from __future__ import print_function

import sys
sys.path.append('..')

from inputs import get_gamepad

from ledwall.components import *
from ledwall.games.tetris import Tetris

from ledwall.components.event import *

import time

from ledwall.util import TimeDelta

udp = UDPSender(server='192.168.178.96')
#s = SerialSender()
time.sleep(1)
d = Display(7, 7, udp, framerate=50)
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


def new_piece():
    if t.testOverflowX() != Tetris.VALID_POSITION:
        return

    if t.testOverflowY() != Tetris.VALID_POSITION:
        return

    if t.checkForCollision(t.piece) == Tetris.VALID_POSITION:
        t.writePieceToMatrix(t.piece)
        t.deleteCompleteRows()

        for c in t.getCompletedColumns():
            t.deleteColumn(c)
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


def new_game():
    t.clearMatrix()
    t.new_piece()
    t.update()


def rotate_cw():
    t.rotateCW()
    t.update()


def rotate_ccw():
    t.rotateCCW()
    t.update()


actions = {
    'ABS_HAT0X': {
        -1: move_left,
        1: move_right,
    },
    'ABS_HAT0Y': {
        -1: move_up,
        1: move_down,
    },
    'BTN_THUMB2': {
        1: rotate_cw,
    },
    'BTN_THUMB': {
        1: new_piece,
    },
    'BTN_TRIGGER': {
        1: rotate_ccw,
    },
    'BTN_TOP': {
        1: new_game,
    },
}

ALL_CODES = {'ABS_X','ABS_HAT0X', 'ABS_HAT0Y', 'BTN_THUMB2', 'BTN_THUMB', 'BTN_TRIGGER', 'BTN_TOP', 'BTN_BASE2', 'BTN_BASE'}

t.update()
d.update()

running = True

while running:
    d.update()
    events = get_gamepad()
    for event in events:
        #if event.code in ALL_CODES:
        #print("{} - {} - {}".format(event.code, event.ev_type, event.state))
        
        if event.code == 'ABS_X':
            if event.state == 255:
                move_right()
            elif event.state == 0:
                move_left()
            else:
                d.update()
             
        elif event.code == 'ABS_Y':
            if event.state == 255:
                move_down()
            elif event.state == 0:
                move_up()
            else:
                d.update()
                
        elif event.code == 'BTN_PINKIE':
            if event.state == 1:
                rotate_cw()
            else:
                d.update()
                
        elif event.code == 'BTN_TOP2':
            if event.state == 1:
                rotate_ccw()
            else:
                d.update()
                
        elif event.code == 'BTN_THUMB2':
            if event.state == 1:
                new_piece()
            else:
                d.update()

        elif event.code == 'BTN_BASE4':
            if event.state == 1:
                new_game()
            else:
                d.update()

        elif event.code == 'BTN_BASE2':
            running = False
