from sender import Sender
from color import Color
import os

class ProgMemSender(Sender):
    def __init__(self, path='.'):
        Sender.__init__(self)
        self._path = path

    @property
    def filename(self):
        return "{}_{:d}.h".format(self.panel.id, self.panel.frame)

    @property
    def path(self):
        return self._path

    @property 
    def size(self):
        return len(self.panel._data)

    @property
    def name(self):
        return "{}_{:d}".format(self.panel.id, self.panel.frame)

    def update(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        fd = os.open(os.path.join(self.path,self.filename), os.O_WRONLY | os.O_CREAT)
        try:
            width  = self.panel.columns
            height = self.panel.rows
            os.write(fd, "const uint8_t {}[] PROGMEM = {} 0x{:02x}, 0x{:02x},\n".format(self.name, "{", width, height))
            for i in range(0,self.size,8):
                if self.panel.gammaCorrection:
                    rowdata = Color.gammaCorrection(self.panel._data[i:i+8])
                else:
                    rowdata = self.panel._data[i:i+8]

                bytes = ['0x{:02x}, '.format(b) for b in rowdata]
                os.write(fd, "    {}\n".format(''.join(bytes)))
            os.write(fd, "0x00};\n\n")

        finally:
            os.close(fd)