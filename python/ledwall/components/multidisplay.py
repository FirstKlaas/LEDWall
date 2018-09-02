from .display import WireMode
from .sender import Sender

class RegionSender(Sender):
    def __init__(self, x, y, width, height, delegate):
        self.delegate = delegate
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self._pixbufiter = None
        self.display = None

    @property
    def data(self):
        if not self._pixbufiter:
            self._pixbufiter = PixBufIter(self, self.display)

        return self._pixbufiter
    
    @property
    def gamma_correction(self):
        return self.display._gamma_correction

    @property   
    def count(self):
        return self.width * self.height
        
    def init(self, panel):
        self.display = panel
        self.delegate.init(self)

    def update(self):
        self.delegate.update()

class PixBufIter():
    def __init__(self, parent, display):
        self.display = display
        self.parent = parent

    @property
    def mode(self):
        return self.display._mode

    @property
    def width(self):
        return self.parent.width

    @property
    def height(self):
        return self.parent.height

    def __getitem__(self, key):
        x,y = key

        if self.mode == WireMode.ZIGZAG:
            return self.display[(self.parent.x + (self.width-x-1),  self.parent.y + y)]

        return self.display[(self.parent.x + x, self.parent.y + y)]

    def __iter__(self):
        for dy in range(self.height):
            for dx in range(self.width):
                color = self[(dx,dy)]
                yield color[0]
                yield color[1]
                yield color[2]

    @property
    def count(self):
        return self.width * self.height

    def __len__(self):
        return self.count * 3
