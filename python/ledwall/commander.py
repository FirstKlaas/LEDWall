class RemotePanel(object):
	def __init__(self, port='/dev/ttyAC0', baudrate=115200):
		self._port     = port
		self._baudrate = baudrate

	@property
	def baudrate(self):
		return self._baudrate

	@property
	def port(self):
		return self._port

	def sendData(data):
		pass


