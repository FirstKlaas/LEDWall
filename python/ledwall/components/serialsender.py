from sender import Sender
from color import Color

import serial

class SerialSender(Sender):

    def __init__(self, portName='/dev/ttyACM0', baudrate=500000):
        Sender.__init__(self)
        self._baudrate   = baudrate
        self._port       = portName
        self._s          = serial.Serial(self.port,self.baudrate)  
        
    @property
    def baudrate(self):
        return self._baudrate

    @property
    def port(self):
        return self._port

    def init(self,panel):
        Sender.init(self,panel)
        self._sendbuffer = bytearray(3*self.panel.count+1)
        #print "COL:{}; ROWS:{}".format(self.panel.columns,self.panel.rows)
        data = [Sender.CMD_INIT_PANEL, self.panel.columns, self.panel.rows]
        #print data
        #print "Buffer has size of {} bytes. Number of leds is {} ".format(len(self._sendbuffer), self.panel.count)
        #print "Panel dimensions are {}x{}".format(self.panel.columns,self.panel.rows)
        self._s.write(bytearray(data))
        #print self._s.readline();

    def update(self):
        #print "Updating frame {}".format(self.panel.frame)
        if not self._s: 
            raise ValueError('Not initialized')

        self._sendbuffer[0] = Sender.CMD_PAINT_PANEL
        for i in range(len(self.panel._data)):
            self._sendbuffer[i+1] = Color.gammaCorrection(self.panel._data[i]) if self.panel.gamma_correction else self.panel._data[i]

        if self._s:
            #print "Sending {} bytes. Data is {}".format(len(self._sendbuffer),[x for x in self._sendbuffer])
            self._s.write(self._sendbuffer)
        else:
            print "No serial line"


