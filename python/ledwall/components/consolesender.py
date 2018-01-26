from sender import Sender

class ConsoleSender(Sender):
    def __init__(self):
        Sender.__init__(self)

    def init(self, panel):
        Sender.init(self,panel)

    def update(self):
        print "Panel {} in frame nr.{:d}".format(self.panel.id, self.panel.frame)