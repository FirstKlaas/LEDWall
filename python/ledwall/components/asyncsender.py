from threading import Thread, Lock

from sender import Sender

class AsyncSender(Sender):
    def __init__(self, delegate):
        """New asnchronous sender.
        This sender takes another sender as a delegate and calls the corresponding update 
        method in a separate thread.
        """
        Sender.__init__(self)
        if not isinstance(delegate,Sender):
            raise ValueError('The delegate must implement the Sender interface.')
        self._delegate = delegate
        self._lock = Lock()

    def update(self):
        self._lock.acquire()
        t = Thread(target=self._delegate.update())
        t.start()
        self._lock.release()

    def init(self, panel):
        Sender.init(self,panel)
        self._delegate.init(panel)


