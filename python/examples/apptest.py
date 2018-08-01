#!/usr/bin/env python3

import sys
sys.path.append('..')

import ledwall.components as comp

s = comp.UDPSender(server='192.168.178.96')
d = comp.Display(7, 7, s)

class MyApp(comp.Application):
	def __init__(self,d,f):
		super().__init__(d,f)

	def paint(self):
		print(self.frame)

app = MyApp(d,20)
app.start_loop()
