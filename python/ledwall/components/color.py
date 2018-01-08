import colorsys

gamma8_table = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
                  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
                  2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
                  5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
                 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
                 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
                 25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
                 37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
                 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
                 69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
                 90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
                115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
                144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
                177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
                215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]



class Color(object):

    @staticmethod
    def gammaCorrection(val):
        return gamma8_table[val]

    @staticmethod
    def fromRGB(r=0, g=0, b=0):
        return Color(r,g,b)

    @staticmethod
    def fromTuple(t):
        return Color.fromRGB(t[0], t[1], t[2])

    @staticmethod
    def fromHexString(color):
        s = color.lstrip('#')
        return Color.fromRGB(int(s[0:2],16),int(s[2:4],16), int(s[4:6],16))

    def __init__(self, r=0, g=0, b=0):
        self.red   = r
        self.green = g
        self.blue  = b

    def __iter__(self):
        yield self._r
        yield self._g
        yield self._b

    def asArray(self):
        return [self.red,self.green,self.blue]
    
    def __repr__(self):
        return 'Color(%d,%d,%d)' % (self.red,self.green,self.blue)
    
    def __str__(self):
        return self.hexStr

    def __eq__(self, other):
        if isinstance(other, Color):
            return (other.red == self.red 
                and other.green == self.green 
                and other.blue == self.blue)
        if ((isinstance(other, tuple) or isinstance(other, list))
            and len(other) == 3):
            return (self.red == other[0] 
                and self.green == other[1]
                and self.blue == other[2] )   
        return NotImplemented

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
    def hexStr(self):
        return "#%0.2X%0.2X%0.2X" % (self._r, self._g, self._b)

    @property
    def hsv(self):
        hsvf = colorsys.rgb_to_hsv(self.red / 255.0, self.green / 255.0,self.blue / 255.0)
        arr = [int(round(x*255)) for x in hsvf]
        return tuple(arr)


    @hexStr.setter
    def hexStr(self, value):
        c = Color.fromHexString(value)
        self._r = int(c.red)
        self._g = int(c.green)
        self._b = int(c.blue)

    @property
    def gamma8(self):
        return (Color.gammaCorrection(self.red),Color.gammaCorrection(self.green),Color.gammaCorrection(self.blue))

    def __getitem__(self, key):
        if isinstance(key,str):
            if key == 'red' or key == 'r': return self.red
            if key == 'green' or key == 'g': return self.green
            if key == 'reblue' or key == 'b': return self.blue
            raise ValueError('Uknown string identifier to lookup item',key)                
            
        else:
            if isinstance(key,int):
                if key < 0 or key > 2:
                    raise ValueError('Index out ouf bounds [0,2]', key)

            elif isinstance(key, slice):
                if abs(key.start) > 2:
                    raise ValueError('Slice start ouf bounds [-2,2]', key)
                
            return self.asArray()[key]
    
