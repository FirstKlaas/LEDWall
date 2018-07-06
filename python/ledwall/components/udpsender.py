from __future__ import print_function
from __future__ import division
from sender import Sender
from color import Color

import socket
import time


class UDPSender(Sender):

    def __init__(self, server='localhost', port=3548, framerate=25):
        Sender.__init__(self)
        self._server = server
        self._port = port
        self._delay = 1.0 / framerate

    @property
    def baudrate(self):
        return self._baudrate

    @property
    def port(self):
        return self._port

    def init(self, panel):
        Sender.init(self, panel)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sendbuffer = bytearray(3 * self.panel.count + 4)
        self._sendbuffer[0] = 2 # Write Raw
        self._sendbuffer[1] = 2 # Update
        self._sendbuffer[2] = self.panel.count
        self._sendbuffer[3] = 0 # Reserved

    def update(self):
        if not self._socket:
            raise ValueError('Not initialized')

        for i in range(len(self.panel.data)):
            if self.panel.gamma_correction:
                self._sendbuffer[i + 4] = Color.gammaCorrection(self.panel.data[i])
            else:
                self._sendbuffer[i + 4] = self.panel.data[i]

        if self._socket:
            time.sleep(self._delay)
            self._socket.sendto(self._sendbuffer, (self._server, self._port))
        else:
            raise ValueError("No Socket Connection")
