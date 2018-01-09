import colorsys

class RGBColor(object):

    @staticmethod
    def fromIntValues(r,g,b):
        return RGBColor(r / 255., g / 255., b / 255)

    def __init__(self, r, g, b):
        self._r = float(r)
        if self._r < 0.0 or self._r > 1.0:
            raise ValueError("Red value out of range.", r)

        self._g = float(g)
        if self._g < 0.0 or self._g > 1.0:
            raise ValueError("Green value out of range.", g)

        self._b = float(b)
        if self._b < 0.0 or self._b > 1.0:
            raise ValueError("Green value out of range.", b)

    def __str__(self):
        return '({:.2f},{:.2f},{:.2f})'.format(self.red, self.green, self.blue)

    def __repr__(self):
        return 'RGBColor({:.2f},{:.2f},{:.2f})'.format(self.red, self.green, self.blue)
        
    def __iter__(self):
        yield self._r
        yield self._g
        yield self._b
    
    @property
    def intValues(self):
        return (self.red * 255., self.blue * 255., self.green * 255.)

    @property
    def red(self):
        return self._r

    @red.setter
    def red(self,value):
        self._r = int(value)
        if self._r < 0 or self._r > 255:
            raise ValueError('Only values between 0 and 255 are accepted for the red channel',value)

    @property
    def green(self):
        return self._g

    @green.setter
    def green(self,value):
        self._g = int(value)
        if self._g < 0 or self._g > 255:
            raise ValueError('Only values between 0 and 255 are accepted for the green channel',value)

    @property
    def blue(self):
        return self._b

    @blue.setter
    def blue(self,value):
        self._b = int(value)
        if self._b < 0 or self._b > 255:
            raise ValueError('Only values between 0 and 255 are accepted for the blue channel',value)

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(self.red, self.green,self.blue)

