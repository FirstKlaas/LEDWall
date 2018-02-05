from ledwall.components import *
from ledwall.games.tetris import Tetris

from inputs import get_gamepad
import time

#d = Display(7,7,MqttSender())
s = SerialSender()
#print "WAIT"
time.sleep(5)
d = Display(7,7,s)
t = Tetris(d)

t.update()

run = True

def quit():
	global run
	run = False

def moveRight():
	p = t._currentPiece
	if t.testOverflowX(p,dx=1) == Tetris.VALID_POSITION:
		p['x'] += 1
		t.update()

def moveLeft():
	p = t._currentPiece
	if t.testOverflowX(p,dx=-1) == Tetris.VALID_POSITION:
		p['x'] -= 1
		t.update()

def moveUp():
	p = t._currentPiece
	if t.testOverflowY(p,dy=-1) == Tetris.VALID_POSITION:
		p['y'] -= 1
		t.update()

def newPiece():
	if t.checkForCollision(t._currentPiece) == Tetris.VALID_POSITION:
		t.writePieceToMatrix(t._currentPiece)
		t.deleteCompleteRows()
		# TODO: Create an animation for the columns an rows to be
		# deleted.
		for c in t.getCompletedColumns():
			t.deleteColumn(c)
		t._currentPiece = t.getNewPiece()
		t.update()

def moveDown():
	p = t._currentPiece
	overflow = t.testOverflowY(p,dy=1)
	# When moving down, an overflow at the top is acceptable.
	# This is alwas true at the very beginning for every new piece,
	# because they start above the display.
	if overflow in [Tetris.VALID_POSITION,Tetris.OVERFLOW_TOP]:
		p['y'] += 1
		t.update()

def newGame():
	t.clearMatrix()
	t._currentPiece = t.getNewPiece()
	t.update()

def rotateCW():
	t.rotateCW()
	t.update()

def rotateCCW():
	t.rotateCCW()
	t.update()

actions =  {
	'ABS_HAT0X' : {
		-1 : moveLeft,
		 1 : moveRight,
	},
	'ABS_HAT0Y' : {
		-1 : moveUp,
		 1 : moveDown,
	},
	'BTN_THUMB2' : {
		1 : rotateCW,
	},
	'BTN_THUMB' : {
		1 : newPiece,
	},
	'BTN_TRIGGER' : {
		1 : rotateCCW,
	},
	'BTN_TOP' : {
		1 : newGame,
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
