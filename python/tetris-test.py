from ledwall.components import *
from ledwall.games.tetris import Tetris

display = Display(7,7,MqttSender(), framerate=1, async=True)
game = Tetris(display)

bg = HSVColor(0.0,1.0,0.4)
hueDelta = 0.01

while True:
	display.fill(bg)
	game.drawPiece(game.getNewPiece())
	display.update()
	bg._h += hueDelta 