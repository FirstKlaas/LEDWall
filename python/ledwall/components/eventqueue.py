import threading


class Event(object):
    GAMEPAD = 1
    KEYBOARD = 2
    MOUSE = 3
    SYSTEM = 4
    USER = 999

    def __init__(self, event_type, action, data={}):
        self._event_type = event_type
        self._data = data
        self._action = action

    @property
    def type(self):
        return self._event_type

    @property
    def action(self):
        return self._action

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value


class EventQueue(object):

    def __init__(self):
        self._lock = threading.Lock
        self._events = []

    def put(self, event, high_priority=False):
        with self._lock:
            if high_priority:
                self._events.insert(0, event)
            else:
                self._events.append(event)

    @property
    def empty(self):
        with self._lock:
            return len(self._events) == 0

    def get(self):
        with self._lock:
            self._events.pop(0)
