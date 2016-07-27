import time
import quantities as q

class timer(object):
    def __init__(self):
        self.prev = time.time()
        self.times = []

    def now(self):
        return time.time()

    def dt(self):
        now = time.time()
        return now - self.prev

    def record(self):
        now = time.time()
        self.times.append(now - self.prev)
        return self.times[-1]

    def flush(self):
        now = time.time()
        self.times.append(now - self.prev)
        times = self.times
        self.times = []
        return times

    def reset(self):
        now = time.time()
        dt = now - self.prev
        self.prev = now
        return dt

def BrianToQuantity(bq):
    spl = str(bq).split(" ")
    if len(spl)==1: spl = ["1"]+spl
    qq = q.Quantity(float(spl[0]), units=spl[1])
    return qq