import colorsys

def __int(fval):
	return int(round(fval))

class HSVColor(object):
	@staticmethod
	def fromTuple(val):
		return HSVColor(val[0],val[1],val[2])

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

	def toRGB(self):
		rgbf = colorsys.hsv_to_rgb(self.h,self.s,self.v)
		return (__int(rgb[0]),__int(rgb[1]),__int(rgb[2]))