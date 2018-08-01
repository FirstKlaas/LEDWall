from ledwall.util import TimeDelta
from .eventqueue import EventEmitter, Event


class FramerateEmitter(EventEmitter):
    def __init__(self, framerate):
        # type : (int) -> None
        super().__init__()
        self._millis_per_frame = 1000.0 / framerate
        self._timer = TimeDelta()
        self._timer.begin()
        self._frame = 1

    def emit(self):
        self._timer.measure()
        if self._timer.millis >= self._millis_per_frame:
            self.queue.put(Event(Event.SYSTEM, 'update', {'frame': self._frame}, priority=Event.PRIORITY_HIGH))
            self._frame += 1
            self._timer.begin()

