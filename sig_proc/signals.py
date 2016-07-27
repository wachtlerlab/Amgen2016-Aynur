import brian as b
import neo
import numpy as np
import quantities as q




def compare(a, b, precision=1e-9):
    sum = abs(a)+abs(b)
    if abs(a-b)<precision*sum:
        return True
    else: return False



def nearest_multiple(a, d):
    n = int((a/d).simplified)
    return n*d



class SignalBuilder(object):
    def __init__(self, *args, **kwargs):
        if len(args)>0:
            self.props = args[0]
        elif "signal" in kwargs:
            self.props = kwargs["signal"]
        elif "times" in kwargs:
            x = kwargs["times"]
            un = kwargs.get("units")
            if un==None: un=q.dimensionless
            self.props = neo.AnalogSignal([1]*len(x), t_start = x[0], sampling_period=(x[1]-x[0]))
        elif "length" in kwargs:
            sp = kwargs["sampling_period"]
            ts = kwargs["t_start"]
            l = kwargs["length"]
            un = kwargs.get("units")
            if un==None: un=q.dimensionless
            self.props = neo.AnalogSignal([1]*l, t_start=ts, sampling_period=sp, units=un)
        else: raise Exception("cannot create SignalBuilder: input data is not enough")

    def __return_signal__(self, signal, units):
        return neo.AnalogSignal(signal, t_start=self.props.t_start, sampling_period=self.props.sampling_period, units=units)

    def get_constant(self, value = 1.):
        signal = np.array(len(self.props.times)*[1]) * value
        return self.__return_signal__(signal, value.units)

    def get_sine(self, period, shift, units = q.dimensionless):
        signal = np.sin(2*np.pi*(self.props.times - shift)/period)
        return self.__return_signal__(signal, units)

    def get_rect(self, start, stop, units = q.dimensionless):
        signal = np.array((self.props.times <= stop)*(self.props.times >= start), dtype=float)
        return self.__return_signal__(signal, units)

    def get_periodic_rect(self, period, width, shift, units = q.dimensionless):
        tm = self.props.times - shift
        n = np.round(tm / period)
        signal = np.array(np.abs(tm - n * period) * 2 < width, dtype=float)
        return self.__return_signal__(signal, units)

def get_signal(sampling_period, t_start, duration, val=q.Quantity(0)):
    n = int(duration/sampling_period)
    return neo.AnalogSignal([val]*n, units=val.units, t_start=t_start, sampling_period=sampling_period)

def TimedArray_from_AnalogSignal(sig):
    return b.TimedArray(arr = sig.simplified.magnitude, times = sig.times.simplified.magnitude)

def AnalogSignalFromTimes(times, signal, units=q.dimensionless, name=None, description=None):
    sp = (times[-1]-times[0])/len(times)
    res = neo.AnalogSignal(signal, t_start=times[0], sampling_period=sp, units=units, name=name, description=description)
    return res

def ShiftSignal(sig, dtime):
    return neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]+dtime, sampling_period=sig.sampling_period, units=sig.units)

def ShiftSignalNull(sig, dtime):
    s = nearest_multiple(dtime, sig.sampling_period)
    print s
    n = int(s/sig.sampling_period)
    res = neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]+s, sampling_period=sig.sampling_period, units=sig.units)
    res2 = neo.AnalogSignal(n*[0*sig.units], t_start=sig.times[0], sampling_period=sig.sampling_period, units=sig.units)
    return Concat(res, res2)

def BeginSignalOn(sig, time):
    return neo.AnalogSignal(sig.magnitude, t_start=time, sampling_period = sig.sampling_period, units = sig.units)


def ReInit(magnitude, t_start, sampling_period, units):
    return neo.AnalogSignal(magnitude, t_start=t_start, sampling_period=sampling_period, units=units)


def ShiftSpikeTrain(spk, dtime):
    return neo.SpikeTrain(spk.times + dtime, spk.t_stop-dtime, spk.units)


def Concat(sig1, sig2):
    if sig1.times[0]<sig2.times[0]:
        x = sig1
        y = sig2
    else:
        x = sig2
        y = sig1
    dtx = x.times[1]-x.times[0]
    dty = y.times[1]-y.times[0]
    if not compare(dtx, dty): raise Exception("sample_periods don't match")
    flt = ((y.times[0]-x.times[0])/x.sampling_period)
    fbo = round(flt)
    if not compare(flt, fbo): raise Exception("sample times not match. {0} and {1}, diff={2}".format(fbo, flt, fbo-flt))
    t_start = x.times[0]
    t = x.times < y.times[0]
    dist = int((y.times[0]-x.times[-1])/x.sampling_period) - 1
    xdata = x.simplified
    ydata = y.simplified
    if dist>0: data = np.concatenate((xdata.magnitude[t], np.array([0.]*dist), ydata.magnitude))
    else: data = np.concatenate((xdata.magnitude[t], ydata.magnitude))
    return neo.AnalogSignal(data, t_start=t_start, sampling_period=x.sampling_period, units = xdata.units)

def Join(lst):
    an = lst[0]
    for k in lst[1:]:
        an = Concat(an, k)
    return an

def Join_Shifted(lst, dtime = 0*q.s):
    an = lst[0]
    for i in xrange(1, len(lst)):
        an = Concat(an, ShiftSignal(lst[i], dtime*i))
    return an

def JoinSpikeTrains(lst):
    t_stop = max([a.t_stop for a in lst])
    times = q.s*np.concatenate([a.times/q.s for a in lst])
    return neo.SpikeTrain(times, t_stop=t_stop)

def JoinSpikeTrainsShifted(lst, dtime=0*q.s):
    return JoinSpikeTrains([ShiftSpikeTrain(lst[i], i*dtime) for i in xrange(len(lst))])

def Zip(spkl):
    lst = []
    for i in xrange(len(spkl)):
        lst = lst+zip([i]*len(spkl[i].times), spkl[i].times)
    return lst