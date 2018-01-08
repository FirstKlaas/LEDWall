from __future__ import division

try:
    import serial
except ImportError:
    print "Serial not availabe. Use: pip install serial"
    
import time

from color import Color

from ..util import TimeDelta, intersectRect
from ..geometry import *

PIL_AVAILABLE = True

try:
    from PIL import Image
except ImportError:
    print "Python Image library (PIL) not availabe. Image functions will be disabled"

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
    """Construktor. 

    Create a new instance of an led display. The baudrate has to match the baudrate of the arduino sketch.
    Also the portName has to match the name of the port, the arduino is connected to. On windows os based
    systems the name is something like 'COM3'.

    The max value for the baudrate depends on the quality of the USB Cable as well as the length of the cable.
    I tested successfully a baudrate of 1000000.

    A very basic program could look like this:

    .. code-block:: python
    
        from ledwall.components import *

        d = Display(16,32)
        
        red   = Color(255,0,0)
        green = Color(0,255,0)    

        d.fill(green)
        d.setPixel(0,3,red)
        d.setPixel(14,23,red)

        d.update()

    :param cols: The number of columns of the display
    :type cols: int

    :param rows: The number of rows of the display.
    :type rows: int

    :param mode: The mode that the LEDs ar organized. Left-to-Right or Zig-Zag. Defaults to Display.MODE_LTR.
    :type mode: int

    :rtype: None
    """    

    MODE_LTR     = 0
    MODE_ZIGZACK = 1
    
    def __init__(self, cols, rows, mode=MODE_LTR, portName='/dev/ttyACM0', baudrate=1000000, framerate=25): 
        try:
            self._s          = serial.Serial(portName,baudrate)
        except serial.SerialException:
            self._s = None    
        self._cols       = int(cols)
        self._rows       = int(rows)
        self._data       = [0]*(BYTES_PER_PIXEL*self.count)
        self._sendbuffer = bytearray(BYTES_PER_PIXEL*self.count)
        self._baudrate   = baudrate
        self._port       = portName
        self._mode       = mode
        self._lastupdate = None
        self.framerate   = framerate 
        self._transmissionTime = TimeDelta()
        self._framenr          = 0
        self._frameDuration    = TimeDelta()
        
        if self._cols < 1:
            raise ValueException('Argument cols must be a value greater than 1.', cols) 

        if self._rows < 1:
            raise ValueException('Argument rows must be a value greater than 1.', cols)

    def __iter__(self):
        index  = 0
        while index < self.count:
            yield tuple(self._data[index*BYTES_PER_PIXEL:(index+1)*BYTES_PER_PIXEL])
            index += 1

    def __getitem__(self, key):
        if isinstance(key, (tuple, list)) and len(key) == 2:
            index = self._coordsToIndex(key[0], key[1]) * 3
            return tuple(self._data[index:index+3])

        if isinstance(key, int):
            index = key*3    
            return tuple(self._data[index:index+3])

        #TODO support slices

        return NotImplemented


    def _setColorAt(self, index, color):
        if index >= self.count:
            raise ValueError('Index out of range. Maximum is %d but was %d' % (self.count - 1, index))

        index *= BYTES_PER_PIXEL

        if isinstance(color,Color):
            self._data[index]   = color.red
            self._data[index+1] = color.green
            self._data[index+2] = color.blue                        
            return

        if isinstance(color, (list,tuple)) and len(color) > 2:
            self._data[index]   = color[0]
            self._data[index+1] = color[1]
            self._data[index+2] = color[2]
            return

        return NotImplemented

    def __setitem__(self, key, item):
        if not item:
            raise ValueError('None is not allowed for item. Item must be a color instance')

        if isinstance(key, int):
            if key < 0:
                raise ValueError('Index may not below zero.', key, item)

            if key >= self.count:
                raise ValueError('Index must below count.', key, item)

            self._setColorAt(self._adjustIndex(key),item)
            return

        if isinstance(key, (tuple,list)) and len(key) == 2:
            self._setColorAt(self._coordsToIndex(key[0],key[1]), item)   

        if isinstance(key, slice):
            i = key.start
            while i<key.stop:
                if self._setColorAt(i,item) == NotImplemented:
                    return
                i += (key.step or 1)
            return

        return NotImplemented

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

    @property
    def frame(self):
        return self._framenr

    @property
    def framerate(self):
        return self._framerate

    @framerate.setter
    def framerate(self, value):
        self._framerate = value
        self._millis_per_frame = 1000 / value

    @property
    def transmissionInfo(self):
        return self._transmissionTime.asTuple()

    def _testCoords(self, x, y):
        if x < 0 or x >= self.columns:
            return False
        if y < 0 or y >= self.rows:
            return False
        return True

    def _adjustColumn(self, x, y):
        if self._mode == Display.MODE_ZIGZACK and self.oddRow(y):
            return self.columns-x-1

        return x

    def _adjustIndex(self, index):
        return self._coordsToIndex(self._indexToCoords(index,False));

    def _coordsToIndex(self, x, y, adjust=True):        
        if adjust:
            return (y*self.columns) + self._adjustColumn(x,y)
        return (y*self.columns) + x

    def _indexToCoords(self, index, adjust=True):
        x = index % self.columns
        y = index // self.columns
        if adjust:
            return (self._adjustColumn(x,y) ,y)
        return (x ,y)

    def setPixel(self, x, y, color, update=False):
        """Setting the color for a single pixel. 

        Returns True, if setting the pixel was successful, Fales else. The color is specified by a color instance. The method
        also accepts tuples or arrays as colors. The length has to be at least 3 and must contain the value for red, green, and
        blue.

        The following lines have the same effect.

        .. code-block:: python

            d.setPixel(0,3,red,True)
            d.setPixel(0,3,(255,0,0),True)
            d.setPixel(0,3,[255,0,0],True)
            
        :param x: The x position of the pixel. Must be a value with the following constraint: ``0 <= x < width``
        :type x: int

        :param y: The number of rows of the display.
        :type y: int

        :param color: The color for the pixel. If you want to deactivate or clear a pixel, just use black (0,0,0) as color value.
        :type color: Color, tuple, list

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: boolean
        """    
        if not self._testCoords(x,y):
            return False

        self._setColorAt(self._coordsToIndex(x,y), color)
        self.update(update)
        return True

    def getPixel(self,x,y):
        """Getting the color for a single pixel. 

        Returns the color for the pixel located at (x,y). The x value must be within the the range: ``0 <= x < width``. 
        The y value must be with the range: ``0 <= y < height``

        :param x: The x position of the pixel. Must be a value with the following constraint: ``0 <= x < width``
        :type x: int

        :param y: The number of rows of the display.
        :type y: int

        :rtype: Color
        """
        index = self._coordsToIndex(x,y) * 3
        return tuple(self._data[index:index+3])

    def writeBitmask(self, row, value, color1=(266,165.0), color0=(0,0,0)):
        x = 0
        index = self._coordsToIndex(6,row);
        for b in range(self.columns):
            self._setColorAt(index, color1 if value & 1 else color0)
            value >>= 1
            index -= 1

    def hLine(self,row, color, update=False):
        """Drawing a horizontal line in the specified color. 

        The row value must be with the range: ``0 <= row < height``

        :param row: The row to be filled.
        :type row: int

        :param color: The color for the row. If you want to deactivate or clear a row, just use black (0,0,0) as color value.
        :type color: Color, tuple, list

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if (row < 0) or (row >= self.rows):
            raise ValueError('Rowindex out of bounds.', row)
        self[row*self.columns:((row+1)*self.columns)] = color    
        self.update(update)

    def vLine(self, column, color, update=False):
        """Drawing a vertical line in the specified color. 

        The column value must be with the range: ``0 <= column < width``

        :param column: The column to be filled.
        :type column: int

        :param color: The color for the column. If you want to deactivate or clear a row, just use black (0,0,0) as color value.
        :type color: Color, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if (column < 0) or (column >= self.columns):
            raise ValueError('Columnindex out of bounds.', column)

        for i in range(self.rows):
            self._setColorAt(self._coordsToIndex(column,i), color)

        self.update(update)

    def oddRow(self,row):
        return (row & 1) == 1

    def shiftRowRight(self, row, update=False):
        """Shifts all pixels in the specified row to the right.

        The method shift pixels to the right visually, because the method takes the mode into account. This means, if
        the mode is ``Display.MODE_ZIGZAG`` and the row number is odd, then the pixela are shifted physically to the left.
        But because this row reads left to right, the pixels are shifted visually to the right.

        The pixel to the outermost right will be placed at the first column. So this method implements a rotation of the pixels.

        :param row: The number of the row to be shifted. The row value must be with the range: ``0 <= row < height``
        :type column: int

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if self.oddRow(row) and self._mode == Display.MODE_ZIGZACK:
            savedPixel = self.getPixel(self.columns-1,row)
            index = self._coordsToIndex(0,row, False) * 3
            self._data[index:index + (self.columns-1) * 3] = self._data[index+3: index + (self.columns) * 3]
            self.setPixel(0,row,savedPixel)

        else:
            savedPixel = self.getPixel(self.columns-1,row) 
            index = self._coordsToIndex(0,row) * 3
            self._data[index+3: index+self.columns * 3] = self._data[index:index + (self.columns-1) * 3]
            self.setPixel(0,row,savedPixel)

        self.update(update)

    def shiftRight(self, update=False):
        """Shifts all pixels to the right.

        The method shift pixels to the right visually, because the method takes the mode into account. This means, if
        the mode is ``Display.MODE_ZIGZAG`` and the row number is odd, then the pixela are shifted physically to the left.
        But because this row reads left to right, the pixels are shifted visually to the right.

        The pixel to the outermost right will be placed at the first column. So this method implements a rotation of the pixels.

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        for row in range(self.rows):
            self.shiftRowRight(row)

        self.update(update)

    def asRectangle(self):
        return Rectangle(0,0,self.columns, self.rows)

    def fillRect(self, x, y, w, h, color, update=False):
        """ Fills a rectangle in the specified color

        :param color: The color for the rectangle. If you want to deactivate or clear a rectangle, just use black (0,0,0) as color value.
        :type color: Color, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        rect = Rectangle(x,y,w,h)
        rect -= self.asRectangle()

        if rect:
            rect = Rectangle.fromTuple(rect)
            for px in range(rect.x,rect.right):
                for py in range(rect.y, rect.bottom):
                    self.setPixel(px,py,color)
        else:
            print "No intersection found"

        self.update(update)

    def fill(self, color, update=False):
        """Fills the LED display in the specified color.

        :param color: The color for the display. If you want to deactivate or clear the panel, just use black (0,0,0) as color value.
        :type color: Color, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if isinstance(color, Color):
            self._data[::3]  = [color.red] * self.count
            self._data[1::3] = [color.green] * self.count
            self._data[2::3] = [color.blue] * self.count
            self.update(update)
            return

        if isinstance(color, (list,tuple)) and len(color) > 2:
            self._data[::3]  = [color[0]] * self.count
            self._data[1::3] = [color[1]] * self.count
            self._data[2::3] = [color[2]] * self.count
            self.update(update)
            return

        return NotImplemented

    def clear(self, update=False):
        """Clears the display (sets all pixel to black)

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """        
        self._data[:] = [0] * (BYTES_PER_PIXEL*self.count)
        self.update(update)

    def update(self, update=True):
        """Updates the LED display

        The internal framebuffer is send to the arduino board and the LED stripe gets updated.

        The method takes framerate into account. If the time between this update and the last update
        is less then the milliseconds per frame, the method will sleep 'til the end of the frame and 
        update the data at the end of the frame.

        Every time the LED display is updated, the framenumber will be increased by one. 

        .. note::
           If you are interested to see the time consumed by transferring the date to the arduino,
           you can read the ransmissionInfo property after updating. The following code snippet shows
           the basic usage:

        Read out the timings for transmission:

        .. code-block:: python

            d.fill(Color(255,0,0))
            print d.transmissionInfo

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if not update:
            return

        self._framenr += 1
        
        if self._frameDuration.hasStarted:
            self._frameDuration.measure()
            millis = self._frameDuration.millis
            if millis < self._millis_per_frame:
                time.sleep((self._millis_per_frame-millis)/1000)

        self._frameDuration.begin()

        for i in range(len(self._data)):
            self._sendbuffer[i] = Color.gamma8(self._data[i])

        self._transmissionTime.begin()
        if self._s:
            self._s.write(bytearray(self._sendbuffer))
        else:
            print "No serial line"

        self._transmissionTime.measure()


    def showImage(self, path, update=False):
        if 'PIL' not in sys.modules:
            raise ValueError('Module PIL not available. Consider to install PIL to use this function.')
        img = Image.open(path)
        rgbimg = img.convert('RGB')
        for y in range(self.rows):
          for x in range(self.columns):
            self.setPixel(x,y,rgbimg.getpixel((x,y)))
        self.update(update)

    def showImageAt(self, image, src_coords=None, dest_coords=None, transparentColor=None, update=False):
        if 'PIL' not in sys.modules:
            raise ValueError('Module PIL not available. Consider to install PIL to use this function.')
        if not src_coords:
            src_coords = (0,0,self.columns, self.rows)
        '''
        TODO: Den Bereich ermitteln, der gezeichnet werden muss. Das ist eigentlich der Schnittpunkt aus 
        src und dest, sowie dem Panel
        '''
        region = intersectRect(src_coords, dest_coords)
        if not region:
            return None
        region = intersectRect(region, (0,0,self.columns, self.rows))
        if not region:
            return None
        print "Now painting image ... TODO"


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
