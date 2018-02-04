from inputs import get_gamepad
while 1:
	events = get_gamepad()
	for event in events:
		
		print event.ev_type
		print event.code
		print event.state
		print "--------------------------------"