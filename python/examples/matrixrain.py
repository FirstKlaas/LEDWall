from ledwall.components import (Display, HSVColor, RGBColor)

class Drop(object):

	def __init__(self, column, display):
		self._display = display
		if column >= display.columns:
			raise ValueError("Column for drop too big. Out of range for given display.")
		self._column = column
		self._basecolor = HSVColor.fromIntValues(114.,92.8,76.1)
		self._current_color = RGBColor(1.0,1.0,1.0)
		self._row = 0
		self._drop_length = int(display.rows * 1.5)
		self._max_row = display.rows + self._drop_length + 1
		self._color_values = [ 1. / v for v in range(1, self._drop_length+1)]

	def paint(self, display):
		pass
		

