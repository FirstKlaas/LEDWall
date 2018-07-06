
from inputs import get_gamepad
from .eventqueue import EventEmitter, Event


class GamepadEmitter(EventEmitter):
    ALL_CODES = {'ABS_HAT0X', 'ABS_HAT0Y', 'BTN_THUMB2', 'BTN_THUMB', 'BTN_TRIGGER', 'BTN_TOP', 'BTN_BASE2', 'BTN_BASE'}

    def __init__(self):
        EventEmitter.__init__(self)

    def emit(self):
        events = get_gamepad()
        for event in events:
            if event.code in GamepadEmitter.ALL_CODES:
                self.queue.put(Event(Event.GAMEPAD, event.code,
                                 {'ev_type': event.ev_type, 'state': event.state, 'code': event.code}))

