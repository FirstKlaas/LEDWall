from __future__ import print_function
from __future__ import print_function

from .sender import Sender
from .color import Color

import serial
import time

from threading import Lock


class SerialSender(Sender):

    def __init__(self, port_name='/dev/ttyACM0', baudrate=115200):
        super().__init__()
        self._baudrate = baudrate
        self._port = port_name
        self._lock = Lock()
        self._s = serial.Serial(self.port, self.baudrate)   
             

    @property
    def baudrate(self):
        return self._baudrate

    @property
    def port(self):
        return self._port

    def init(self, panel):
        super().init(panel)
        self._sendbuffer = bytearray(3 * self.panel.count + 1)

        # Send command to initialize the panel
        #data = [Sender.CMD_INIT_PANEL, self.panel.columns, self.panel.rows]
        #self._s.write(bytearray(data))

    def update(self):
        if not self._s:
            raise ValueError('Not initialized')

        with self._lock:

            self._sendbuffer[0] = Sender.CMD_PAINT_PANEL
            for i in range(len(self.panel.data)):
                if self.panel.gamma_correction:
                    self._sendbuffer[i + 1] = Color.gammaCorrection(self.panel.data[i])
                else:
                    self._sendbuffer[i + 1] = self.panel.data[i]

            if self._s:
                self._s.write(self._sendbuffer)
            else:
                raise ValueError("No serial line")
