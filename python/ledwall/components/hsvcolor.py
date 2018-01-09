import colorsys

class HSVColor(object):

    @staticmethod
    def fromIntValues(h, s, v):
        return HSVColor(h / 360., s / 100. , v / 100.)

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

    @property
    def intValues(self):
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
        return colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)