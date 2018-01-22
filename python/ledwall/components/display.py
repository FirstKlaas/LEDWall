from __future__ import division

import time
import sys
import itertools

from color import Color

from ..util import TimeDelta, intersectRect
from ..geometry import *

PIL_AVAILABLE = True

try:
    from PIL import Image
except ImportError:
    print "Python Image library (PIL) not availabe. Image functions will be disabled"

BYTES_PER_PIXEL = 3

class Display(object):
    """Construktor. 

    Create a new instance of an led display. The Display class manages the colorstate of the LEDs on the physical panel. The class offers
    a lot of methods to set and change the colors. The physical LEDs are updated via the update() method. Because there are different ways
    to connect the arduino to your computer, the transmission of the data is managed by an instance of a ``Sender``. THis library offers
    several Implementations (SerialSender, MqttSender, TkSender).

    The methods to manipulate the color state of the pixels pay respect to the wiring mode you used.

    A very basic program could look like this:

    .. code-block:: python
    
        from ledwall.components import *


        s = MqttSender()
        d = Display(16,32,s)
        
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

    :param sender: Instance of the sender (One of the subclasses, to be more precise)
    :type sender: ledwall.components.Sender 

    :param mode: The mode that the LEDs ar organized. Left-to-Right or Zig-Zag. Defaults to Display.MODE_LTR.
    :type mode: int

    :rtype: None
    """    

    MODE_LTR          = 0
    MODE_ZIGZAG       = 1

    def __init__(self, cols, rows, sender=None, mode=MODE_LTR, framerate=25, id='LEDPANEL0001'): 
        self._cols       = int(cols)
        self._rows       = int(rows)
        self._data       = [0]*(BYTES_PER_PIXEL*self.count)
        self._mode       = mode
        self._lastupdate = None
        self.framerate   = framerate 
        self._transmissionTime = TimeDelta()
        self._framenr          = 0
        self._frameDuration    = TimeDelta()
        self._gamma_correction = True
        self._id               = id
        self._sender           = sender
        
        if self._cols < 1:
            raise ValueException('Argument cols must be a value greater than 1.', cols) 

        if self._rows < 1:
            raise ValueException('Argument rows must be a value greater than 1.', cols)

        if self._sender:
            self._sender.init(self)

    @property
    def id(self):
        """Returns the ID of this panel.

        :rtype: str
        """
        return self._id

    def changeSaturation(self, val):
        for rgb in self:
            hsv = RGBColor.fromIntValues(rgb[0],rgb[1],rgb[2]).hsv
            hsv = HSVColor(hsv[0],hsv[1],hsv[2])
            print hsv

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

        if isinstance(key, slice):
            return [color for color in itertools.islice(self, key.start, key.stop, key.step)]

        return NotImplemented


    def _setColorAt(self, index, color):
        if index >= self.count:
            raise ValueError('Index out of range. Maximum is %d but was %d' % (self.count - 1, index))

        index *= BYTES_PER_PIXEL

        color = Color.convert(color)
        self._data[index]   = color.red
        self._data[index+1] = color.green
        self._data[index+2] = color.blue                        
        return

    def setColors(self, colors, transparentColor = None):
        index = 0
        for c in colors:
            if c and c != transparentColor:
                self._setColorAt(index,c)
            index += 1
    
    def getColors(self):
        return self[:]
                    
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
            i    = key.start or 0
            n    = 0
            stop = key.stop or self.count
            step = key.step or 1
            while i<stop:
                if self._setColorAt(i,item[n]) == NotImplemented:
                    return
                i += step
                n += 1
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
    def byteCount(self):
        return len(self._data)

    @property
    def transmissionInfo(self):
        return self._transmissionTime.asTuple()

    @property
    def gammaCorrection(self):
        return self._gamma_correction

    @gammaCorrection.setter
    def gammaCorrection(self, value):
        self._gamma_correction = value
            
    def _testCoords(self, x, y):
        if x < 0 or x >= self.columns:
            return False
        if y < 0 or y >= self.rows:
            return False
        return True

    def _adjustColumn(self, x, y):
        if self._mode == Display.MODE_ZIGZAG and self.oddRow(y):
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
        return Color.fromTuple(tuple(self._data[index:index+3]))

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
        self[row*self.columns:((row+1)*self.columns)] = Color.convert(color)    
        self.update(update)

    def vLine(self, column, color, update=False):
        """Drawing a vertical line in the specified color. 

        The column value must be with the range: ``0 <= column < width``

        :param column: The column to be filled.
        :type column: int

        :param color: The color for the column. If you want to deactivate or clear a row, just use black (0,0,0) as color value.
        :type color: Color, RGBColor, HSVColor, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if (column < 0) or (column >= self.columns):
            raise ValueError('Columnindex out of bounds.', column)
        
        color = Color.convert(color)

        for i in range(self.rows):
            self._setColorAt(self._coordsToIndex(column,i), color)

        self.update(update)

    def oddRow(self,row):
        return (row & 1) == 1

    def shiftRowLeft(self, row, update=False):
        startIndex = row * self.columns * 3

        if self.oddRow(row) and self._mode == Display.MODE_ZIGZAG:
            width = self.columns * 3
            rightPixel = self._data[startIndex+width-3:startIndex+width]
            tmp = self._data[startIndex:startIndex+width-3]
            self._data[startIndex + 3:startIndex+width] = tmp
            self._data[startIndex:startIndex+3] = rightPixel[:]

        else:
            width = self.columns * 3
            leftPixel = self._data[startIndex:startIndex+3]
            self._data[startIndex:startIndex+width-3] = self._data[startIndex+3:startIndex+width]
            self._data[startIndex+width-3:startIndex+width] = leftPixel[:]
            
        self.update(update)

    def shiftLeft(self, update=False):
        for row in range(self.rows):
            self.shiftRowLeft(row)

        self.update(update)
            
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
        startIndex = row * self.columns * 3

        if self.oddRow(row) and self._mode == Display.MODE_ZIGZAG:
            width = self.columns * 3
            leftPixel = self._data[startIndex:startIndex+3]
            self._data[startIndex:startIndex+width-3] = self._data[startIndex+3:startIndex+width]
            self._data[startIndex+width-3:startIndex+width] = leftPixel[:]

        else:
            width = self.columns * 3
            rightPixel = self._data[startIndex+width-3:startIndex+width]
            tmp = self._data[startIndex:startIndex+width-3]
            self._data[startIndex + 3:startIndex+width] = tmp
            self._data[startIndex:startIndex+3] = rightPixel[:]
            
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

    @property
    def bounds(self):
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
        color = Color.convert(color)
        self._data[::3]  = [color.red] * self.count
        self._data[1::3] = [color.green] * self.count
        self._data[2::3] = [color.blue] * self.count
        self.update(update)

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
        self._transmissionTime.begin()
        if self._sender:
            self._sender.update()

        self._transmissionTime.measure()

    def showImage(self, path, update=False, transparentColor=None):
        self.loadImage(path, update, transparentColor)

    def loadImage(self, path, update=False, transparentColor=None):
        """Loads an image into the LED buffer.

        The method loads an image located at *path* into the LED buffer. If a transparent
        color is provided, all *trasparent* colors are ignored. If *update = True* the panel
        data will be updated immediately.

        :param path: The relative or absolute path to the image. The method uses the PIL library
            for reading the file. So any filetype supported by PIL is supported by this method.
        :type path: str

        :param update: If True, the panel gets updated via the sender component. Defaults to False
        :type update: boolean
        
        :param transparentColor: The color which defines transparency. Defaults to None.
        :type transparentColor: tuple
        """    
        if 'PIL' not in sys.modules:
            raise ValueError('Module PIL not available. Consider to install PIL to use this function.')
        img = Image.open(path)
        rgbimg = img.convert('RGB')
        for y in range(self.rows):
          for x in range(self.columns):
            color = rgbimg.getpixel((x,y))
            if transparentColor != color:
                self.setPixel(x,y,color)
        self.update(update)

    def copyRegionFrom(self, src, rectSrc=None, poindDst=Point(0,0), transparentColor=None, update=False):
        if not rectSrc:
            rectSrc = Rectangle(0,0, self.columns, self.rows)

        for x in range(rectSrc.width):
            for y in range(rectSrc.height):
                color = src.getPixel(rectSrc.x + y, rectSrc.y + y)
                if color and color != transparentColor:
                    self.setPixel(pointDst.x+x, pointDst.y+y, color)

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
