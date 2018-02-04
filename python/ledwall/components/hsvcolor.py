import colorsys

class HSVColor(object):
    """Represents a color in the HSV color space.
    The components of the HSV color are normalized to the
    intervall [0.0;1.0].

    If you have in values to create a HSVColor you can use
    the class method fromIntValues to create an instance.

    The hue component has to be within the range of [0;360]. Saturation
    and value in the range of [0;100]

    The rgb property returns the converted and normalized values in the
    RGB color space.

    """

    @staticmethod
    def fromIntValues(h, s, v):
        return HSVColor(h / 360., s / 100. , v / 100.)

    def __init__(self, h=0.0, s=0.0, v=0.0):
        """Creates a new color instance in the HSV color space. 
        The values for hue, value and saturation have to be provided 
        in normalized [0.0;1.0] form.
        """
        self._h = h
        self._v = v
        self._s = s

    @property
    def hue(self):
        """The normalized hue component of the color.
        
        :rtype: float
        """ 
        return self._h

    @hue.setter
    def hue(self, value):
        self.h = value

    @property
    def h(self):
        """Same as the property hue. Just for the lazy people.
        
        :rtype: float
        """
        return self._h

    @h.setter
    def h(self, value):
        self._h = value
        self._h %= 1.0
        
    @property
    def saturation(self):
        """The normalized saturation component of the color.
        
        :rtype: float
        """         
        return self._s

    @saturation.setter
    def saturation(self, val):
        self.s = val
    
    @property
    def s(self):
        """Same as the property saturation. Just for the lazy people.
        
        :rtype: float
        """
        return self._s

    @s.setter
    def s(self, val):
        self._s += val
        self._s %= 1.0

    @property
    def value(self):
        """The normalized value component of the color.
        
        :rtype: float
        """         
        return self._v

    @value.setter
    def value(self, val):
        self.v = val

    @property
    def v(self):
        """Same as the property value. Just for the lazy people.
        
        :rtype: float
        """
        return self._v

    @v.setter
    def v(self, val):
        self._v += val
        self._v %= 1.0

    @property
    def intValues(self):
        """Returns the int values for the three components. The
        normalized hue value is projected on the intervall [0;360]
        and value and saturation are projeted on the intervall
        [0;100]

        :rtype: tuple(int)
        """
        return (int(round(self.hue * 360.)), int(round(self.saturation * 100.)), int(round(self.value * 100.)))

    def __iter__(self):
        yield self.h
        yield self.s
        yield self.v
        
    def __repr__(self):
        return 'HSVColor({:.2f},{:.2f},{:.2f})'.format(self.h,self.s,self.v)
    
    def __str__(self):
        return '({:.2f},{:.2f},{:.2f})'.format(self.h,self.s,self.v)

    def __getitem__(self, key):
        if isinstance(key,str):
            if key == 'hue' or key == 'h': return self.h
            if key == 'saturation' or key == 's': return self.s
            if key == 'value' or key == 'v': return self.v
            raise ValueError('Uknown string identifier to lookup item',key)                
            
        else:
            if isinstance(key,int):
                if key < 0 or key > 2:
                    raise ValueError('Index out ouf bounds [0,2]', key)

            elif isinstance(key, slice):
                if abs(key.start) > 2:
                    raise ValueError('Slice start ouf bounds [-2,2]', key)
                
            return self.asArray()[key]
 
    @property
    def rgb(self):
        """Returns a tuple with the converted and normalized rgb values

        :rtype: tuple(float)
        """
        return colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)