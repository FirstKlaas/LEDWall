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

    def __repr__(self):
        return 'HSVColor(%d,%d,%d)' % (self.h,self.s,self.v)
    
    def __str__(self):
        return 'H(%d,%d,%d)' % (self.h,self.s,self.v)

    @property
    def floatValues(self):
        return (self.h / 360.0, self.s / 100.0,self.v / 100.0)

    @property
    def rgb(self):
        values = self.floatValues
        rgbf = colorsys.hsv_to_rgb(values[0], values[1], values[2])
        return (HSVColor._convert(rgbf[0]),HSVColor._convert(rgbf[1]),HSVColor._convert(rgbf[2]))

    @property
    def color(self):
        return Color.fromTuple(self.rgb)