from __future__ import (print_function, division)

from .sender import Sender
from .color import Color

import socket

class UDPSender(Sender):

    def __init__(self, server='localhost', port=3548, framerate=25):
        super().__init__()
        self._server = server
        self._port = port
        self._delay = 1.0 / framerate

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    def init(self, panel):
        super().init(panel)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sendbuffer = bytearray(3 * self.panel.count + 4)
        self._sendbuffer[0] = 2 # Write Raw
        self._sendbuffer[1] = 2 # Update
        self._sendbuffer[2] = self.panel.count
        self._sendbuffer[3] = 0 # Reserved

    def update(self):
        if not self._socket:
            raise ValueError('Not initialized')

        for i, value in enumerate(self.panel.data):
            if self.panel.gamma_correction:
                self._sendbuffer[i + 4] = Color.gammaCorrection(value)
            else:
                self._sendbuffer[i + 4] = value

        if self._socket:
            try:
                self._socket.sendto(self._sendbuffer, (self._server, self._port))
            except Exception as e:
                print("Could not send data via udp. ", e)
        else:
            raise ValueError("No Socket Connection")
