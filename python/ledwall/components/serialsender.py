from sender import Sender
from color import Color

import serial

class SerialSender(Sender):

    def __init__(self, portName='/dev/ttyACM0', baudrate=1000000):
        Sender.__init__(self)
        self._baudrate   = baudrate
        self._port       = portName

    @property
    def baudrate(self):
        return self._baudrate

    @property
    def port(self):
        return self._port

    def init(self,panel):
        Sender.init(self,panel)
        self._s          = serial.Serial(portName,baudrate)  
        self._sendbuffer = bytearray(3*self.panel.count+1)
        self._s.write(bytearray([Sender.CMD_INIT_PANEL, self.panel.columns, self.panel.rows]))

    def update(self):
        if not self._s: 
            raise ValueError('Not initialized')

        self._sendbuffer[0] = Sender.CMD_PAINT_PANEL
        for i in range(len(self.panel._data)):
            self._sendbuffer[i+1] = Color.gammaCorrection(self.panel._data[i]) if self.panel.gammaCorrection else self.panel._data[i]

        if self._s:
            self._s.write(self._sendbuffer)
        else:
            print "No serial line"


