__all__ = ['Sender']

class Sender(object):

    CMD_INIT_PANEL    =   1
    CMD_CLEAR_PANEL   =   2
    CMD_FILL_PANEL    =   3
    CMD_PAINT_PANEL   =   4
    CMD_SET_PIXEL     =   5
    CMD_WRITE_RAW     =   6
    CMD_SHOW          = 255

    def __init__(self):
        self._panel = None

    @property
    def panel(self):
        return self._panel

    def init(self, panel):
        self._panel = panel

    def update(self):
        pass

