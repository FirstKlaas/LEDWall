from ledwall.components.event import EventDispatcher
from ledwall.util import TimeDelta


class Application(object):

    def __init__(self, display, framerate):
        # type : (Display) -> None
        self._display = display
        self._millis_per_frame = 1000.0 / framerate
        self._timer = TimeDelta()
        self._timer.begin()
        self._frame = 1
        self._running = True
        self._event_dispatcher = EventDispatcher()

    @property
    def display(self):
        return self._display

    def paint(self):
        pass

    def handle_event(self, event):
        pass

    def start_loop(self):
        while self._running:
            event = queue.next_event()
            if event:
                self.handle_event(event)
            self.update()

    def stop(self):
        self._running = False

    def update(self):
        self._timer.measure()
        if self._timer.millis >= self._millis_per_frame:
            self._display.update()
            self._frame += 1
            self._timer.begin()
