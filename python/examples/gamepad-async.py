from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')

import ledwall.components.event as ev

dp = ev.EventDispatcher()
dp.add_emitter(ev.GamepadEmitter())
dp.add_emitter(ev.FramerateEmitter(1))

while True:
	event = dp.next_event()
	if event:
		print(event);
	