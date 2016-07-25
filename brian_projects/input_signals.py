from brian_projects.NeuronModels.M import *

def gen_time_interval(start, end, step):
    return arange(start, end, step)

def gen_constant_signal(X, val):
    return array([val]*len(X))

class Filter(object):
    def __init__(self, func):
        self.func = func
    def on(self, X, Y):
        leng = min(len(X), len(Y))
        Z = zeros(leng)
        for i in xrange(leng):
            Z[i] = self.func(X[i], Y[i])
        return Z

class SingleRectFilter(Filter):
    def __init__(self, start, end):
        super(SingleRectFilter, self).__init__(lambda x, y: y if x >= start and x <= end else 0)

class PeriodicRectFilter(Filter):
    def __init__(self, period, width, shift):
        def func(x, y):
            n = round((x - shift)/period)
            if abs(x-shift-n*period)*2 < width:
                return y
            else: return 0.
        super(PeriodicRectFilter, self).__init__(func)

class PeriodicSineFilter(Filter):
    def __init__(self, period, shift):
        print pi
        super(PeriodicSineFilter, self).__init__(lambda x, y: y*sin((x-shift)*2.*pi/period))

class VolFilter(Filter):
    def __init__(self, val):
        super(VolFilter, self).__init__(lambda x, y: val*y)

def TR(Y, d1, dt, d2):
    return TimedArray(Y*d1, dt=dt*d2)

def sum_signals(x, y):
    return x+y