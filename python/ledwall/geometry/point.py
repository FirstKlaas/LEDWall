class Point(object):
	def __init__(self, x, y):
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value

	@property
	def position(self):
		return (self.x, self.y)	

	def __len__(self):
		return 2

	def __getitem__(self, key):
		return {
			0 : self.x,
			1 : self.y,
		}.get(key,None)

	def __iter__(self):
		yield self.x
		yield self.y
	
