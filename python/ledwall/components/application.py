from ..components.event import *
from ..util import TimeDelta


class Application(object):

    def __init__(self, display, framerate):
        # type : (Display) -> None
        self._display = display
        self._framerate = framerate
        self._running = True
        self._event_dispatcher = EventDispatcher()
        if framerate and framerate > 0:
            self._event_dispatcher.add_emitter(FramerateEmitter(framerate))

    @property
    def display(self):
        return self._display

    @property
    def frame(self):
        return self.display.frame
        
    def paint(self):
        pass

    def handle_event(self, event):
        pass

    def start_loop(self):
        while self._running:
            event = self._event_dispatcher.next_event()
            if (event.type, event.action) == (Event.SYSTEM,'update'):
                self.update()
            else:
                self.handle_event(event)

    def stop(self):
        self._running = False

    def update(self):
        self.paint()
        self._display.update()
