class TimeDelta(object):

    def __init__(self):
        self._max    = None
        self._min    = None
        self._millis = None
        self._begin  = None

    @property
    def hasStarted(self):
        return self._begin is not None

    def begin(self):
        self._begin = datetime.datetime.now()

    def measure(self):
        if not self.hasStarted:
            return None

        diff = datetime.datetime.now() - self._begin
        self._millis = diff.total_seconds() * 1000
        self._min = min(self._min, self._millis) if self._min else self._millis            
        self._max = max(self._max, self._millis) if self._max else self._millis
        return (self._millis,self._min,self._max)

    @property 
    def millis(self):
        return self._millis

    @property 
    def min(self):
        return self._min

    @property 
    def max(self):
        return self._max

    def _NoneOrStr(self, val):
        return "%.2f" % val if val else "-"

    def asTuple(self):
        return (self.millis, self.min, self.max)

    def __str__(self):
        return "(ms: %s, min: %s, max: %s)" % (self._NoneOrStr(self._millis),self._NoneOrStr(self._min),self._NoneOrStr(self._max))

