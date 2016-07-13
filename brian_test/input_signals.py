import numpy as np
from M import *

def gen_time_interval(start, end, step=1.):
    return np.arange(start, end, step)

def gen_constant_signal(X, val):
    return np.array([val]*len(X))

class Filter(object):
    def __init__(self, func):
        self.func = func
    def on(self, X, Y):
        leng = min(len(X), len(Y))
        Z = np.zeros(leng)
        for i in xrange(leng):
            Z[i] = self.func(X[i], Y[i])

class QuadraticFilter(Filter):
    def __init__(self, start, end):
        super(QuadraticFilter, self).__init__(lambda x, y: 0. if x<start or x>end else y)

class Vol(Filter):
    def __init__(self, val):
        super(Filter, self).__init__(lambda x, y: val*y)

def TR(Y, dt):
    return TimedArray(Y, dt=dt)