import colorsys

from color import Color

class HSVColor(object):

	@staticmethod
	def fromTuple(val):
		return HSVColor(val[0],val[1],val[2])

	@staticmethod
	def _convert(fval):
		return int(round(255. * fval))

	def __init__(self, h, s, v):
		self._h = h
		self._v = v
		self._s = s

	@property
	def hue(self):
		return self._h

	@property
	def h(self):
		return self._h

	@property
	def saturation(self):
		return self._s

	@property
	def s(self):
		return self._s

	@property
	def value(self):
		return self._v

	@property
	def v(self):
		return self._v

	def __iter__(self):
		yield self.h
		yield self.s
		yield self.v

	@property
	def rgb(self):
		rgbf = colorsys.hsv_to_rgb(self.h / 360.0, self.s / 100.0,self.v / 100.0)
		return (HSVColor._convert(rgbf[0]),HSVColor._convert(rgbf[1]),HSVColor._convert(rgbf[2]))

	@property
	def color(self):
		return Color.fromTuple(self.rgb)