from __future__ import division
from __future__ import print_function

import time
import sys
import itertools

from color import Color

from ..util import TimeDelta
from ..geometry import *
from asyncsender import AsyncSender

PIL_AVAILABLE = True

try:
    from PIL import Image
except ImportError:
    Image = None
    print("Python Image library (PIL) not availabe. Image functions will be disabled")

BYTES_PER_PIXEL = 3


class Display(object):
    """Constructor.

    Create a new instance of an led display. The Display class manages the color state of the LEDs on the physical
    panel. The class offers a lot of methods to set and change the colors. The physical LEDs are updated via the
    :meth:`~ledwall.components.Display.update` method. Because there are different ways to connect the arduino to your
    computer, the transmission of the data is managed by an instance of a :class:`~ledwall.components.Sender`.
    This library offers several Implementations (:class:`~ledwall.components.SerialSender`,
    :class:`~ledwall.components.MqttSender`).

    The methods to manipulate the color state of the pixels pay respect to the wiring mode you used.

    A very basic program could look like this:

    .. code-block:: python
    
        from ledwall.components import *


        s = MqttSender()
        d = Display(16,32,s)
        
        red   = Color(255,0,0)
        green = Color(0,255,0)    

        d.fill(green)
        d.set_pixel(0,3,red)
        d.set_pixel(14,23,red)

        d.update()

    :param cols: The number of columns of the display
    :type cols: int

    :param rows: The number of rows of the display.
    :type rows: int

    :param sender: Instance of the sender (One of the subclasses, to be more precise)
    :type sender: Sender 

    :param mode: The mode that the LEDs ar organized. Left-to-Right or Zig-Zag. Defaults to Display.MODE_LTR.
    :type mode: int

    :rtype: None
    """    

    MODE_LTR = 0
    MODE_ZIGZAG = 1

    def __init__(self, cols, rows, sender=None, mode=MODE_LTR, framerate=25, panel_id='LEDPANEL0001', async=False):
        self._cols = int(cols)
        self._rows = int(rows)
        self._data = [0]*(BYTES_PER_PIXEL*self.count)
        self._mode = mode
        self._last_update = None
        self._framerate = 0
        self._millis_per_frame = 0.0
        self.framerate = framerate
        self._transmissionTime = TimeDelta()
        self._frame_nr = 0
        self._frameDuration = TimeDelta()
        self._gamma_correction = True
        self._id = panel_id
        self._sender = sender
        if sender and async:
            self._sender = AsyncSender(sender)
        
        if self._cols < 1:
            raise ValueError('Argument cols must be a value greater than 1.', cols)

        if self._rows < 1:
            raise ValueError('Argument rows must be a value greater than 1.', cols)

        if self._sender:
            self._sender.init(self)

    @property
    def data(self):
        return self._data

    @property
    def id(self):
        """The panel id as set in the constructor. (read-only)
        """
        return self._id

    def __iter__(self):
        index = 0
        while index < self.count:
            yield tuple(self._data[index*BYTES_PER_PIXEL:(index+1)*BYTES_PER_PIXEL])
            index += 1

    def __getitem__(self, key):
        if isinstance(key, (tuple, list)) and len(key) == 2:
            index = self._coords_to_index(key[0], key[1]) * 3
            return tuple(self._data[index:index+3])

        if isinstance(key, int):
            index = key*3    
            return tuple(self._data[index:index+3])

        if isinstance(key, slice):
            return [color for color in itertools.islice(self, key.start, key.stop, key.step)]

        return NotImplemented

    def _set_color_at(self, index, color):
        if index >= self.count:
            raise ValueError('Index out of range. Maximum is %d but was %d' % (self.count - 1, index))

        index *= BYTES_PER_PIXEL

        color = Color.convert(color)
        self._data[index] = color.red
        self._data[index+1] = color.green
        self._data[index+2] = color.blue                        
        return

    def set_colors(self, colors, transparent_color=None):
        index = 0
        for c in colors:
            if c and c != transparent_color:
                self._set_color_at(index, c)
            index += 1
    
    def get_colors(self):
        return self[:]
                    
    def __setitem__(self, key, item):
        if not item:
            raise ValueError('None is not allowed for item. Item must be a color instance')

        if isinstance(key, int):
            if key < 0:
                raise ValueError('Index may not below zero.', key, item)

            if key >= self.count:
                raise ValueError('Index must below count.', key, item)

            self._set_color_at(self._adjust_index(key), item)
            return

        if isinstance(key, (tuple, list)) and len(key) == 2:
            self._set_color_at(self._coords_to_index(key[0], key[1]), item)

        if isinstance(key, slice):
            i = key.start or 0
            n = 0
            stop = key.stop or self.count
            step = key.step or 1
            while i < stop:
                if self._set_color_at(i, item[n]) == NotImplemented:
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
        return self._frame_nr

    @property
    def framerate(self):
        return self._framerate

    @framerate.setter
    def framerate(self, value):
        self._framerate = value
        self._millis_per_frame = 1000 / value

    @property
    def byte_count(self):
        return len(self._data)

    @property
    def transmission_info(self):
        return self._transmissionTime.asTuple()

    @property
    def gamma_correction(self):
        return self._gamma_correction

    @gamma_correction.setter
    def gamma_correction(self, value):
        self._gamma_correction = value
            
    def _test_coords(self, x, y):
        if x < 0 or x >= self.columns:
            return False
        if y < 0 or y >= self.rows:
            return False
        return True

    def _adjust_column(self, x, y):
        """

        :param int x: X position
        :param int y: Y position
        :return: The adjusted column index.
        """
        if self._mode == Display.MODE_ZIGZAG and self.odd_row(y):
            return self.columns-x-1

        return x

    def _adjust_index(self, index):
        x, y = self._index_to_coords(index, False)
        return self._coords_to_index(x, y)

    def _coords_to_index(self, x, y, adjust=True):
        if adjust:
            return (y*self.columns) + self._adjust_column(x, y)
        return (y*self.columns) + x

    def _index_to_coords(self, index, adjust=True):
        x = index % self.columns
        y = index // self.columns
        if adjust:
            return self._adjust_column(x, y), y
        return x, y

    def set_pixel(self, x, y, color, update=False):
        """Setting the color for a single pixel. 

        Returns True, if setting the pixel was successful, Fales else. The color is specified by a color instance.
        The method also accepts tuples or arrays as colors. The length has to be at least 3 and must contain the
        value for red, green, and blue.

        The following lines have the same effect.

        .. code-block:: python

            d.set_pixel(0,3,red,True)
            d.set_pixel(0,3,(255,0,0),True)
            d.set_pixel(0,3,[255,0,0],True)
            
        :param x: The x position of the pixel. Must be a value with the following constraint: ``0 <= x < width``
        :type x: int

        :param y: The number of rows of the display.
        :type y: int

        :param color: The color for the pixel. If you want to deactivate or clear a pixel, just use black (0,0,0)
        as color value.
        :type color: Color, tuple, list

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: boolean
        """    
        if not self._test_coords(x, y):
            return False

        self._set_color_at(self._coords_to_index(x, y), color)
        self.update(update)
        return True

    def get_pixel(self, x, y):
        """Getting the color for a single pixel. 

        Returns the color for the pixel located at (x,y). The x value must be within the the range: ``0 <= x < width``. 
        The y value must be with the range: ``0 <= y < height``

        :param x: The x position of the pixel. Must be a value with the following constraint: ``0 <= x < width``
        :type x: int

        :param y: The number of rows of the display.
        :type y: int

        :rtype: Color
        """
        index = self._coords_to_index(x, y) * 3
        return Color.fromTuple(tuple(self._data[index:index+3]))

    def write_bitmask(self, row, value, color1=(266, 165.0), color0=(0, 0, 0)):
        index = self._coords_to_index(6, row)
        for b in range(self.columns):
            self._set_color_at(index, color1 if value & 1 else color0)
            value >>= 1
            index -= 1

    def horizontal_line(self, row, color, update=False):
        """Drawing a horizontal line in the specified color. 

        The row value must be with the range: ``0 <= row < height``

        :param row: The row to be filled.
        :type row: int

        :param color: The color for the row. If you want to deactivate or clear a row, just use black (0,0,0)
        as color value.
        :type color: Color, tuple, list

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if (row < 0) or (row >= self.rows):
            raise ValueError('Row index out of bounds.', row)
        self[row*self.columns:((row+1)*self.columns)] = Color.convert(color)    
        self.update(update)

    def vertical_line(self, column, color, update=False):
        """Drawing a vertical line in the specified color. 

        The column value must be with the range: ``0 <= column < width``

        :param column: The column to be filled.
        :type column: int

        :param color: The color for the column. If you want to deactivate or clear a row, just use black (0,0,0)
        as color value.
        :type color: Color, RGBColor, HSVColor, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if (column < 0) or (column >= self.columns):
            raise ValueError('Column index out of bounds.', column)
        
        color = Color.convert(color)

        for i in range(self.rows):
            self._set_color_at(self._coords_to_index(column, i), color)

        self.update(update)

    @staticmethod
    def odd_row(row):
        """

        :param int row: Test, if the index of the row is even (False) or odd (True)
        :return: True, if row is odd, False else.
        """
        return (row & 1) == 1

    def shift_row_left(self, row, update=False):
        start_index = row * self.columns * 3

        if self.odd_row(row) and self._mode == Display.MODE_ZIGZAG:
            width = self.columns * 3
            right_pixel = self._data[start_index + width - 3:start_index + width]
            tmp = self._data[start_index:start_index + width - 3]
            self._data[start_index + 3:start_index + width] = tmp
            self._data[start_index:start_index + 3] = right_pixel[:]

        else:
            width = self.columns * 3
            left_pixel = self._data[start_index:start_index + 3]
            self._data[start_index:start_index + width - 3] = self._data[start_index + 3:start_index + width]
            self._data[start_index + width - 3:start_index + width] = left_pixel[:]
            
        self.update(update)

    def shift_left(self, update=False):
        for row in range(self.rows):
            self.shift_row_left(row)

        self.update(update)
            
    def shift_row_right(self, row, update=False):
        """Shifts all pixels in the specified row to the right.

        The method shift pixels to the right visually, because the method takes the mode into account. This means, if
        the mode is ``Display.MODE_ZIGZAG`` and the row number is odd, then the pixels are shifted physically to the
        left. But because this row reads left to right, the pixels are shifted visually to the right.

        The pixel to the outermost right will be placed at the first column. So this method implements a rotation of
        the pixels.

        :param row: The number of the row to be shifted. The row value must be with the range: ``0 <= row < height``
        :type row: int

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        start_index = row * self.columns * 3

        if self.odd_row(row) and self._mode == Display.MODE_ZIGZAG:
            width = self.columns * 3
            left_pixel = self._data[start_index:start_index+3]
            self._data[start_index:start_index+width-3] = self._data[start_index+3:start_index+width]
            self._data[start_index+width-3:start_index+width] = left_pixel[:]

        else:
            width = self.columns * 3
            right_pixel = self._data[start_index+width-3:start_index+width]
            tmp = self._data[start_index:start_index+width-3]
            self._data[start_index + 3:start_index+width] = tmp
            self._data[start_index:start_index+3] = right_pixel[:]
            
        self.update(update)

    def shift_right(self, update=False):
        """Shifts all pixels to the right.

        The method shift pixels to the right visually, because the method takes the mode into account. This means, if
        the mode is ``Display.MODE_ZIGZAG`` and the row number is odd, then the pixela are shifted physically to the
        left. But because this row reads left to right, the pixels are shifted visually to the right.

        The pixel to the outermost right will be placed at the first column. So this method implements a rotation of
        the pixels.

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        for row in range(self.rows):
            self.shift_row_right(row)

        self.update(update)

    def as_rectangle(self):
        return Rectangle(0, 0, self.columns, self.rows)

    @property
    def bounds(self):
        """Returns a Rectangle instance where width is equal
        to the number of columns and height ist equal to the 
        number of rows.

        :return: Rectangle with a size equal to the size of this display.
        :rtype: Rectangle
        """
        return Rectangle(0, 0, self.columns, self.rows)
        
    def fill_rect(self, x, y, w, h, color, update=False):
        """ Fills a rectangle in the specified color

        :param int x: X position of the top left corner

        :param int y: Y position of the top left corner

        :param int w: Width of the rectangle

        :param int h: Height of the rectangle

        :param color: The color for the rectangle. If you want to deactivate or clear a rectangle, just use
        black (0,0,0) as color value.
        :type color: Color, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        rect = Rectangle(x, y, w, h)
        rect -= self.as_rectangle()

        if rect:
            rect = Rectangle.fromTuple(rect)
            for px in range(rect.x, rect.right):
                for py in range(rect.y, rect.bottom):
                    self.set_pixel(px, py, color)
        else:
            print("No intersection found")

        self.update(update)

    def fill(self, color, update=False):
        """Fills the LED display in the specified color.

        :param color: The color for the display. If you want to deactivate or clear the panel, just use
        black (0,0,0) as color value.
        :type color: Color, tuple, list
        
        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        color = Color.convert(color)
        self._data[::3] = [color.red] * self.count
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

        The internal frame buffer is send to the arduino board and the LED stripe gets updated.

        The method takes framerate into account. If the time between this update and the last update
        is less then the milliseconds per frame, the method will sleep 'til the end of the frame and 
        update the data at the end of the frame.

        Every time the LED display is updated, the frame number will be increased by one.

        .. note::
           If you are interested to see the time consumed by transferring the date to the arduino,
           you can read the transmissionInfo property after updating. The following code snippet shows
           the basic usage:

        Read out the timings for transmission:

        .. code-block:: python

            d.fill(Color(255,0,0))
            print d.transmission_info

        :param update: If True, the display will be updated.
        :type update: boolean

        :rtype: None
        """
        if not update:
            return

        self._frame_nr += 1
        
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

    def show_image(self, path, update=False, transparent_color=None):
        self.load_image(path, update, transparent_color)

    def load_image(self, path, update=False, transparent_color=None):
        """Loads an image into the LED buffer.

        The method loads an image located at *path* into the LED buffer. If a transparent
        color is provided, all *transparent* colors are ignored. If *update = True* the panel
        data will be updated immediately.

        :param path: The relative or absolute path to the image. The method uses the PIL library
            for reading the file. So any file type supported by PIL is supported by this method.
        :type path: str

        :param update: If True, the panel gets updated via the sender component. Defaults to False
        :type update: boolean
        
        :param transparent_color: The color which defines transparency. Defaults to None.
        :type transparent_color: tuple
        """    
        if 'PIL' not in sys.modules:
            raise ValueError('Module PIL not available. Consider to install PIL to use this function.')
        img = Image.open(path)
        rgbimg = img.convert('RGB')
        for y in range(self.rows):
            for x in range(self.columns):
                color = rgbimg.getpixel((x, y))
                if transparent_color != color:
                    self.set_pixel(x, y, color)
        self.update(update)

    def copy_region_from(self, src, rect_src=None, point_dst=Point(0, 0), transparent_color=None, update=False):
        """Copy a region from another display. If a transparent color is provided, all pixels in the
        source panel with the corresponding color will be ignored. 

        The region specified by the :class:'~ledwall.geometry.Rectangle'*rectSrc* will be copied to 
        position specified by *pointDst*. The parameter *pointDst* defaults to the upper left corner 
        :class:'~ledwall.geometry.Point'(0,0).

        :param Display src: The source display to copy the color values from.

        :param Rectangle rect_src: The position and the size of the region to copy. If no value is provided,
        it defaults to the size of self and position 0,0

        :param Point point_dst: Where to copy to. Defaults to (0,0)

        :param Color transparent_color: Color to ignore while copying. Defaults to None

        :param boolean update: Update display after this operation. Defaults to False
        """
        if not rect_src:
            rect_src = Rectangle(0, 0, self.columns, self.rows)

        for x in range(rect_src.width):
            for y in range(rect_src.height):
                color = src.get_pixel(rect_src.x + x, rect_src.y + y)
                if color and color != transparent_color:
                    self.set_pixel(point_dst.x + x, point_dst.y + y, color)
        self.update(update)
