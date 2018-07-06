from __future__ import print_function
from ledwall.components import *
from ledwall.games.tetris import Tetris

from ledwall.components.event import *

import time

from ledwall.util import TimeDelta

udp = UDPSender(server='192.168.178.96')
#s = SerialSender()
time.sleep(1)
d = Display(7, 7, udp)
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

t.update()

queue = EventDispatcher()

# queue.add_emitter(FramerateEmitter(15))
queue.add_emitter(GamepadEmitter())

running = True


class Framerate(object):
    def __init__(self, framerate):
        # type : (int) -> None
        self._millis_per_frame = 1000.0 / framerate
        self._timer = TimeDelta()
        self._timer.begin()
        self._frame = 1

    def update(self, s):
        self._timer.measure()
        if self._timer.millis >= self._millis_per_frame:
            s.update()
            self._frame += 1
            self._timer.begin()


fr = Framerate(3)
while running:
    fr.update(s)
    event = queue.next_event()
    if event:
        if event.type == event.SYSTEM:
            if event.action == 'update':
                d.update()

        elif event.type == event.GAMEPAD:
            # print(event.action)
            if event.action == 'BTN_BASE2':
                running = False
            elif event.action in actions:
                action = actions[event.action]
                if event['state'] in action:
                    action[event['state']]()
                    s.update()

queue.stop()
