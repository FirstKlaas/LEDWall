from __future__ import print_function
from ledwall.components.event import EventDispatcher, FramerateEmitter, GamepadEmitter

queue = EventDispatcher()

queue.add_emitter(FramerateEmitter(0.5))
queue.add_emitter(GamepadEmitter())

for i in range(20):
    evt = queue.next_event()
    print("Event: %r" % evt)

queue.stop()
