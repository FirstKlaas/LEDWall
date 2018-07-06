from __future__ import print_function
import threading


class Event(object):
    GAMEPAD = 1
    KEYBOARD = 2
    MOUSE = 3
    SYSTEM = 4
    MQTT = 5
    ARDUINO = 6
    USER = 999

    NAMES = {
        GAMEPAD: 'GAMEPAD',
        KEYBOARD: 'KEYBOARD',
        MOUSE: 'MOUSE',
        SYSTEM: 'SYSTEM',
        USER: 'USER',
    }

    def __init__(self, event_type, action, data={}):
        """

        :param str action: The human readable event action
        :param dict data: Dictionary with additional type specific information
        :param int event_type: The 'source' of the event.
        """
        # type: (int, str, dict) -> None
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

    def __str__(self):
        return self._action

    def __repr__(self):
        return "Event('%s','%s',{%d})" % (Event.NAMES[self._event_type], self._action, len(self._data))


class EventQueue(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._events = []

    def put(self, event, high_priority=False):
        with self._lock:
            if high_priority:
                self._events.insert(0, event)
            else:
                self._events.append(event)
            # self._lock.notify()

    def stop(self):
        self.put(EventDispatcher.STOP_EVENT, True)

    @property
    def empty(self):
        with self._lock:
            return len(self._events) == 0

    def get(self):
        with self._lock:
            if len(self._events) == 0:
                # self._lock.wait()
                return None
            return self._events.pop(0)


class EventDispatcher(object):

    def __init__(self):
        self._queue = EventQueue()
        self._generators = []

    def add_emitter(self, src):
        self._generators.append(src)
        src.connect_queue(self._queue)

    def next_event(self):
        """
        Returns the next event object. If no events are in the queue, the method blocks
        until a new event was added to the queue.

        :return: The event object.
        """
        return self._queue.get()

    def stop(self):
        for g in self._generators:
            g.stop()


class EventEmitter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = None
        self._is_running = False

    def connect_queue(self, q):
        self.queue = q
        self._is_running = True
        self.start()

    def stop(self):
        self._is_running = False

    def run(self):
        while self._is_running:
            self.emit()

    def emit(self):
        pass
