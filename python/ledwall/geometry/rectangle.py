from point import Point
from ledwall.util import intersectRect

class Rectangle(Point):
	
	@staticmethod
	def fromTuple(t):
		if len(t) < 4:
			raise ValueError("Cannot create rectangle from given value",t)
		return Rectangle(t[0],t[1],t[2],t[3])
			
	def __init__(self, x, y, width, height):
		Point.__init__(self,x,y)
		self._width  = width
		self._height = height

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, w):
		self._width = w

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, h):
		self._height = h;

	@property
	def right(self):
		return self.x + self.width	

	@property
	def bottom(self):
		return self.y + self.height

	def __len__(self):
		return 4

	def __getitem__(self, key):
		return {
			0 : self.x,
			1 : self.y,
			2 : self.width,
			3 : self.height,
			2 : self.right,
			3 : self.bottom
		}.get(key,None)

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.width
		yield self.height

	def __sub__(self, other):
		return intersectRect(tuple(self),tuple(other))	

	def __rsub__(self, other):
		return intersectRect(tuple(other),tuple(self))	
