from ledwall.components import *
from ledwall.games.tetris import Tetris

from inputs import get_gamepad
import time

s = SerialSender()
time.sleep(5)
d = Display(7, 7, s, framerate=25)
t = Tetris(d)

t.update()

run = True


def stop_game():
    global run
    run = False


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
            # Animate deletion
            t.dissolveColumn(c)
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

"""
"""

t.update()

while run:
    events = get_gamepad()
    for event in events:
        if event.code in actions:
            action = actions[event.code]
            if event.state in action:
                action[event.state]()
