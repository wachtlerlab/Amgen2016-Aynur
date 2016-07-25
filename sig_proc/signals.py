import brian as b
import neo
import numpy as np
import quantities as q

class SignalBuilder(object):
    def __init__(self, *args, **kwargs):
        if len(args)>0:
            self.props = args[0]
        elif "signal" in kwargs:
            self.props = kwargs["signal"]
        elif "times" in kwargs:
            x = kwargs["times"]
            self.props = neo.AnalogSignal([1]*len(x), t_start = x[0], sampling_period=(x[1]-x[0]))
        elif "length" in kwargs:
            sp = kwargs["sampling_period"]
            ts = kwargs["t_start"]
            l = kwargs["length"]
            self.props = neo.AnalogSignal([1]*l, t_start=ts, sampling_period=sp)
        else: raise Exception("cannot create SignalBuilder: input data is not enough")

    def __return_signal__(self, signal, units):
        return neo.AnalogSignal(signal, t_start=self.props.t_start, sampling_period=self.props.sampling_period, units=units)

    def get_constant(self, value = 1.):
        signal = np.array(len(self.props.times)*[1]) * value
        return self.__return_signal__(signal, value.units)

    def get_sine(self, period, shift, units = q.dimensionless):
        signal = units*np.sin(2*np.pi*(self.props.times - shift)/period)
        return self.__return_signal__(signal, units)

    def get_rect(self, start, stop, units = q.dimensionless):
        signal = units*np.array((self.props.times <= stop)*(self.props.times >= start), dtype=float)
        return self.__return_signal__(signal, units)

    def get_periodic_rect(self, period, width, shift, units = q.dimensionless):
        tm = self.props.times - shift
        n = np.round(tm / period)
        signal = units*np.array(np.abs(tm - n * period) * 2 < width, dtype=float)
        return self.__return_signal__(signal, units)


def TimedArray_from_AnalogSignal(sig):
    return b.TimedArray(arr = sig.magnitude, times = sig.times)


def ShiftSignal(sig, dtime):
    return neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]-dtime, sampling_period=sig.sampling_period, units=sig.units)


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
    print dtx, dty
    if x.sampling_period!=y.sampling_period: raise Exception("sample_periods don't match")
    flt = ((y.times[0]-x.times[0])/x.sampling_period)
    if int(flt)!=flt: raise Exception("sample times not match. {0} and {1}".format(int(flt), flt))
    t_start = x.times[0]
    t = x.times < y.times[0]
    dist = int((y.times[0]-x.times[-1])/x.sampling_period) - 1
    if dist>0: data = x.units*np.concatenate((x.magnitude[t], np.array([0.]*dist), y.magnitude))
    return neo.AnalogSignal(data, t_start=t_start, sampling_period=dtx, units = x.units)

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