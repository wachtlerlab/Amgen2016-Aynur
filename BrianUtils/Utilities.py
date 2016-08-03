import json
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
    return QuantityFromString(str(bq))

def QuantityFromString(stri):
    spl = stri.split(" ")
    if len(spl)==1: spl = ["1"]+spl
    return q.Quantity(float(spl[0]), units=spl[1])


def one_layer_fromdict(stri, d, a, dolists = True):
    for k in d:
        nstr = stri+"_"+k if stri!='' else k
        if type(d[k])==dict:
            one_layer_fromdict(nstr, d[k], a, dolists)
        elif type(d[k])==list:
            if dolists:
                one_layer_fromlist(nstr, d[k], a)
            else: a[nstr] = "\n".join(map(str, d[k]))
        else:   a[nstr] = d[k]


def one_layer_fromlist(stri, l, a):
    for i in xrange(len(l)):
        nstr = stri+"_" + str(i) if stri!='' else str(i)
        if type(l[i])==dict:
            one_layer_fromdict(nstr, l[i], a, False)
        elif type(l[i])==list:
            one_layer_fromlist(nstr, l[i], a)
        else:   a[nstr] = l[i]


def one_layer_fromfile(filename, name, dolists=True):
    a = {}
    with open(filename) as f:
        d = json.load(f)
    one_layer_fromdict(name, d, a, dolists)
    return a