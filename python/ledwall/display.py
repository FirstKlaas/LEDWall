from __future__ import division
import serial
import time
import datetime

class Color(object):

    @staticmethod
    def fromRGB(r=0, g=0, b=0):
        return Color(r,g,b)

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

    @hexStr.setter
    def hexStr(self, value):
        c = Color.fromHexString(value)
        self._r = int(c.red)
        self._g = int(c.green)
        self._b = int(c.blue)

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
    
class ColorTable(object):

    AliceBlue      = Color.fromHexString('#F0F8FF')
    Amethyst       = Color.fromHexString('#9966CC')
    AntiqueWhite   = Color.fromHexString('#FAEBD7')
    Aqua           = Color.fromHexString('#00FFFF')
    Aquamarine     = Color.fromHexString('#7FFFD4')
    Azure          = Color.fromHexString('#F0FFFF')
    Beige          = Color.fromHexString('#F5F5DC')
    Bisque         = Color.fromHexString('#FFE4C4')
    Black          = Color.fromHexString('#000000')
    BlanchedAlmond = Color.fromHexString('#FFEBCD')
    Blue           = Color.fromHexString('#0000FF')
    BlueViolet     = Color.fromHexString('#8A2BE2')
    Brown          = Color.fromHexString('#A52A2A')
    BurlyWood      = Color.fromHexString('#DEB887')
    CadetBlue      = Color.fromHexString('#5F9EA0')
    Chartreuse     = Color.fromHexString('#7FFF00')
    Chocolate      = Color.fromHexString('#D2691E')
    Coral          = Color.fromHexString('#FF7F50')
    CornflowerBlue = Color.fromHexString('#6495ED')
    Cornsilk       = Color.fromHexString('#7FFF00')
    Chartreuse     = Color.fromHexString('#FFF8DC')

"""
  Crimson =0xDC143C, Cyan =0x00FFFF, DarkBlue =0x00008B, DarkCyan =0x008B8B,
  DarkGoldenrod =0xB8860B, DarkGray =0xA9A9A9, DarkGrey =0xA9A9A9, DarkGreen =0x006400,
  DarkKhaki =0xBDB76B, DarkMagenta =0x8B008B, DarkOliveGreen =0x556B2F, DarkOrange =0xFF8C00,
  DarkOrchid =0x9932CC, DarkRed =0x8B0000, DarkSalmon =0xE9967A, DarkSeaGreen =0x8FBC8F,
  DarkSlateBlue =0x483D8B, DarkSlateGray =0x2F4F4F, DarkSlateGrey =0x2F4F4F, DarkTurquoise =0x00CED1,
  DarkViolet =0x9400D3, DeepPink =0xFF1493, DeepSkyBlue =0x00BFFF, DimGray =0x696969,
  DimGrey =0x696969, DodgerBlue =0x1E90FF, FireBrick =0xB22222, FloralWhite =0xFFFAF0,
  ForestGreen =0x228B22, Fuchsia =0xFF00FF, Gainsboro =0xDCDCDC, GhostWhite =0xF8F8FF,
  Gold =0xFFD700, Goldenrod =0xDAA520, Gray =0x808080, Grey =0x808080,
  Green =0x008000, GreenYellow =0xADFF2F, Honeydew =0xF0FFF0, HotPink =0xFF69B4,
  IndianRed =0xCD5C5C, Indigo =0x4B0082, Ivory =0xFFFFF0, Khaki =0xF0E68C,
  Lavender =0xE6E6FA, LavenderBlush =0xFFF0F5, LawnGreen =0x7CFC00, LemonChiffon =0xFFFACD,
  LightBlue =0xADD8E6, LightCoral =0xF08080, LightCyan =0xE0FFFF, LightGoldenrodYellow =0xFAFAD2,
  LightGreen =0x90EE90, LightGrey =0xD3D3D3, LightPink =0xFFB6C1, LightSalmon =0xFFA07A,
  LightSeaGreen =0x20B2AA, LightSkyBlue =0x87CEFA, LightSlateGray =0x778899, LightSlateGrey =0x778899,
  LightSteelBlue =0xB0C4DE, LightYellow =0xFFFFE0, Lime =0x00FF00, LimeGreen =0x32CD32,
  Linen =0xFAF0E6, Magenta =0xFF00FF, Maroon =0x800000, MediumAquamarine =0x66CDAA,
  MediumBlue =0x0000CD, MediumOrchid =0xBA55D3, MediumPurple =0x9370DB, MediumSeaGreen =0x3CB371,
  MediumSlateBlue =0x7B68EE, MediumSpringGreen =0x00FA9A, MediumTurquoise =0x48D1CC, MediumVioletRed =0xC71585,
  MidnightBlue =0x191970, MintCream =0xF5FFFA, MistyRose =0xFFE4E1, Moccasin =0xFFE4B5,
  NavajoWhite =0xFFDEAD, Navy =0x000080, OldLace =0xFDF5E6, Olive =0x808000,
  OliveDrab =0x6B8E23, Orange =0xFFA500, OrangeRed =0xFF4500, Orchid =0xDA70D6,
  PaleGoldenrod =0xEEE8AA, PaleGreen =0x98FB98, PaleTurquoise =0xAFEEEE, PaleVioletRed =0xDB7093,
  PapayaWhip =0xFFEFD5, PeachPuff =0xFFDAB9, Peru =0xCD853F, Pink =0xFFC0CB,
  Plaid =0xCC5533, Plum =0xDDA0DD, PowderBlue =0xB0E0E6, Purple =0x800080,
  Red =0xFF0000, RosyBrown =0xBC8F8F, RoyalBlue =0x4169E1, SaddleBrown =0x8B4513,
  Salmon =0xFA8072, SandyBrown =0xF4A460, SeaGreen =0x2E8B57, Seashell =0xFFF5EE,
  Sienna =0xA0522D, Silver =0xC0C0C0, SkyBlue =0x87CEEB, SlateBlue =0x6A5ACD,
  SlateGray =0x708090, SlateGrey =0x708090, Snow =0xFFFAFA, SpringGreen =0x00FF7F,
  SteelBlue =0x4682B4, Tan =0xD2B48C, Teal =0x008080, Thistle =0xD8BFD8,
  Tomato =0xFF6347, Turquoise =0x40E0D0, Violet =0xEE82EE, Wheat =0xF5DEB3,
  White =0xFFFFFF, WhiteSmoke =0xF5F5F5, Yellow =0xFFFF00, YellowGreen =0x9ACD32,
  FairyLight =0xFFE42D, FairyLightNCC =0xFF9D2A
  """

BYTES_PER_PIXEL = 3

class Display(object):
    MODE_LTR     = 0
    MODE_ZIGZACK = 1
    
    def __init__(self, cols, rows, mode=MODE_LTR, portName='/dev/ttyACM0', baudrate=1000000, framerate=25): 
        self._s          = serial.Serial(portName,baudrate)
        self._cols       = int(cols)
        self._rows       = int(rows)
        self._data       = bytearray([0]*(BYTES_PER_PIXEL*self.count))
        self._baudrate   = baudrate
        self._port       = portName
        self._mode       = mode
        self._lastupdate = None
        self._framerate  = framerate 

        self._millis_per_frame = 1000 / framerate
        
        if self._cols < 1:
            raise ValueException('Argument cols must be a value greater than 1.', cols) 

        if self._rows < 1:
            raise ValueException('Argument rows must be a value greater than 1.', cols)

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key, item):
        if not item:
            raise ValueError('None is not allowed for item. Item must be a color instance')

        index = int(key)
        if index < 0:
            raise ValueError('Index may not below zero.', key, item)

        if index >= self.count:
            raise ValueError('Index must below count.', key, item)

        if not isinstance(item, Color):
            raise ValueError('item to set must be an Color instance', key, item)
        
        
        self._data[key] = item
            
    @property
    def columns(self):
        return self._cols

    @property
    def rows(self):
        return self._rows

    @property
    def count(self):
        return self.columns * self.rows

    @property
    def baudrate(self):
        return self._baudrate

    @property
    def port(self):
        return self._port

    def _testCoords(self, x, y):
        if x < 0 or x >= self.columns:
            return False
        if y < 0 or y >= self.rows:
            return False
        return True

    def _coordsToIndex(self, x, y):
        return (y*self.columns*3) + (x*3)

    def setPixel(self, x, y, color):
        if not self._testCoords(x,y):
            raise ValueError('Coordinates out fo Range', x, y)

        index = self._coordsToIndex(x,y)
        self._data[index:index+BYTES_PER_PIXEL] = color.asArray()

    def fill(self, color):
        if isinstance(color, Color):
            self._data[::3]  = [color.red] * self.count
            self._data[1::3] = [color.green] * self.count
            self._data[2::3] = [color.blue] * self.count
            return

        if isinstance(color, (list,tuple)) and len(color) > 2:
            self._data[::3]  = [color[0]] * self.count
            self._data[1::3] = [color[1]] * self.count
            self._data[2::3] = [color[2]] * self.count
            return

        return NotImplemented

    def clear(self):
        self._data[:] = [0] * (BYTES_PER_PIXEL*self.count)
         
    def update(self):
        if self._lastupdate:
            diff = datetime.datetime.now() - self._lastupdate
            millis = diff.total_seconds() * 1000
            if millis < self._millis_per_frame:
                time.sleep(diff.total_seconds())
        self._s.write(self._data)
        self._lastupdate = datetime.datetime.now()

class Palette(object):
    def __init__(self, size):
        self._colors = [ColorTable.Black] * size

    def __getitem__(self, index):
        return self._colors[index]

    def __setitem__(self, key, item):
        if not item:
            raise ValueError('None is not allowed for item. Item must be a color instance')

        index = int(key)
        if index < 0:
            raise ValueError('Index may not below zero.', key, item)

        if index >= len(self._colors):
            raise ValueError('Index must below palette size.', key, item)

        if not isinstance(item, Color):
            raise ValueError('item to set must be an Color instance', key, item)
        
        self._colors[key] = item
