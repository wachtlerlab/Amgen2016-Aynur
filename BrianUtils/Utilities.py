import json
import time
import quantities as q
import brian as b

class timer(object):
    '''
    Class for convinient recording of duration of program. You can use your own, it is just my implementation
    '''
    def __init__(self):
        self.zero = time.time()
        self.times = [self.zero]

    def now(self):
        return time.time() - self.zero

    def dt(self):
        now = time.time()
        return now - self.times[-1]

    def record(self):
        self.times.append(self.now())
        return self.times[-1]

    def flush(self):
        self.times.append(self.now())
        times = self.times
        self.times = [self.now()]
        return times

def BrianToQuantity(bq):
    '''
    Converts brian.Quantity to quantities.Quantity
    :param bq: brian.Quantity
    :return: quantities.Quantity
    '''
    return QuantityFromString(str(bq))

def QuantityFromString(stri):
    '''
    Converts string to quantities.Quantity
    :param stri: string
    :return: quantities.Quantity
    '''
    spl = stri.split(" ")
    if len(spl)==1: spl = ["1"]+spl
    return q.Quantity(float(spl[0]), units=spl[1])

def TimeToBrian(time):
    '''
    converts quantity.Quantity to brian.second
    :param time: quantity.Quantity
    :return: brian.Quantity [brian.second]
    '''
    return float(time.simplified.magnitude)*b.second


def one_layer_fromdict(stri, d, a, dolists = True):
    '''do not use'''
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
    '''do not use'''
    for i in xrange(len(l)):
        nstr = stri+"_" + str(i) if stri!='' else str(i)
        if type(l[i])==dict:
            one_layer_fromdict(nstr, l[i], a, False)
        elif type(l[i])==list:
            one_layer_fromlist(nstr, l[i], a)
        else:   a[nstr] = l[i]


def one_layer_fromfile(filename, name, dolists=True):
    '''do not use'''
    a = {}
    with open(filename) as f:
        d = json.load(f)
    one_layer_fromdict(name, d, a, dolists)
    return a