from ledwall.components import *

#d = Display(7,7,AsyncSender(MqttSender()),framerate=4)
d = Display(7,7,UDPSender(server='192.168.178.96',framerate=20))

color = HSVColor(0.0,1.0,1.0)
deltaHue = 0.01
d.fill(color,True)


while True:
	d._data[3:] = d._data[:-3]
	rgb = Color.fromHSVColor(color)
	d._data[0] = rgb.red
	d._data[1] = rgb.green
	d._data[2] = rgb.blue
	color.hue += deltaHue
	d.update()
