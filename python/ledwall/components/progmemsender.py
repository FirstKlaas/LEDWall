from sender import Sender
import os

class ProgMemSender(Sender):
	def __init__(self, path='.'):
		Sender.__init__(self)
		self._path = path

	@property
	def filename(self):
		return "{}_{:d}".format(self.panel.id, self.panel.frame)

	def update(self):
		fd = os.open(os.join(self.path,filename), os.O_WRONLY | os.O_CREAT)
		try:
			os.write(fd, "Huhu")
		finally:
			os.close(fd)