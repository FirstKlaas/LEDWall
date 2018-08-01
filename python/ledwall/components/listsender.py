from .sender import Sender

class ListSender(Sender):
    """Manages a list of senders, so multiple panelscan be updated 
    by just one display. If async is true, all senders in the delegates
    list are wrapped in an :class:`~ledwall.components.AsyncSender` instance.
    Otherwise the init and update methods are called for each element of
    the list.

    :param delegates: An iterable object of sender instances.
    :type delegates: iterable(Sender)
    :param boolean async: Calls sender asynchronously if True. Directly else.
    """  

    def __init__(self, delegates, async=False):
        super().__init__()
        if async:
            self._delegates = [AsyncSender(s) for s in delegates]
        else:
            self._delegates = delegates

    def init(self, panel):
        """Calls init for every provided sender.
        """
        super().init(panel)
        for s in self._delegates:
            s.init(self.panel)

    def update(self):
        """Calls update for every provided sender.
        """
        for s in self._delegates:
            s.update()

