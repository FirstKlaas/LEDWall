from ledwall.components import (Display)

from ledwall.util import TimeDelta

td = TimeDelta()
d = Display(21,7)

d.show_image('monster.png')

td.begin()
for i in range(10000):
	d.shift_right()

td.measure()
print(td.micros)	