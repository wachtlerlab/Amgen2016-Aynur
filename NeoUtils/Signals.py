import brian as b
import neo
import numpy as np
import quantities as q

def CutFirst(stri):
    stri = str(stri)
    spl = stri.split(" ")
    if len(spl)>2:
        return " ".join(spl[-2:])
    else: return stri

def Compare(a, b, precision=1e-9):
    sum = abs(a)+abs(b)
    if abs(a-b)<precision*sum:
        return True
    else: return False

def NearestDivident(a, d):
    n = int((a/d).simplified)
    return n*d

def QuantityFromString(stri):
    spl = stri.split(" ")
    if len(spl)==1: spl = ["1"]+spl
    elif len(spl)>2: raise Exception("Unsupported quantity format: {0}".format(stri))
    return q.Quantity(float(spl[0]), units=str(spl[1]))

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
            ts = kwargs.get("t_start")
            if ts is None: ts = 0*q.s
            l = kwargs["length"]
            un = kwargs.get("units")
            if un==None: un=q.dimensionless
            self.props = neo.AnalogSignal([1]*l, t_start=ts, sampling_period=sp, units=un)
        else: raise Exception("cannot create SignalBuilder: input data is not enough")

    def __return_signal__(self, signal, units):
        return neo.AnalogSignal(signal, t_start=self.props.t_start, sampling_period=self.props.sampling_period, units=units)

    def get_constant(self, amplitude = 1.*q.dimensionless):
        signal = np.array(len(self.props.times)*[1]) * amplitude.magnitude
        return self.__return_signal__(signal, amplitude.units)

    def get_sine(self, period, shift, amplitude = 1.*q.dimensionless):
        signal = amplitude.magnitude*np.sin(2*np.pi*(self.props.times - shift)/period)
        return self.__return_signal__(signal, amplitude.units)

    def get_rect(self, start, stop, amplitude = 1.*q.dimensionless):
        signal = amplitude.magnitude*np.array((self.props.times <= stop)*(self.props.times >= start), dtype=float)
        return self.__return_signal__(signal, amplitude.units)

    def get_periodic_rect(self, period, width, shift, amplitude = 1.*q.dimensionless):
        tm = self.props.times - shift
        n = np.round(tm / period)
        signal = amplitude.magnitude*np.array(np.abs(tm - n * period) * 2 < width, dtype=float)
        return self.__return_signal__(signal, amplitude.units)

    def get_signal_by_func(self, func, amplitude = 1*q.dimensionless):
        signal = amplitude.magnitude*func(self.props.times)
        return self.__return_signal__(signal, amplitude.units)

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
    return neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]+dtime, sampling_period=sig.sampling_period,
                            units=sig.units, name=sig.name, description=sig.description)

def ShiftSignalNull(sig, dtime):
    s = NearestDivident(dtime, sig.sampling_period)
    n = int(s/sig.sampling_period)
    res = neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]+s, sampling_period=sig.sampling_period, units=sig.units)
    res2 = neo.AnalogSignal(n*[0*sig.units], t_start=sig.times[0], sampling_period=sig.sampling_period, units=sig.units)
    return Concat(res, res2, name=sig.name, description=sig.description)

def BeginSignalOn(sig, time):
    return neo.AnalogSignal(sig.magnitude, t_start=time, sampling_period = sig.sampling_period, units = sig.units,
                            name=sig.name, description=sig.description)


def ReInit(magnitude, t_start, sampling_period, units):
    return neo.AnalogSignal(magnitude, t_start=t_start, sampling_period=sampling_period, units=units)


def ShiftSpikeTrain(spk, dtime):
    return neo.SpikeTrain(spk.times + dtime, spk.t_stop + dtime, spk.units)


def Concat(sig1, sig2, name=None, description=None):
    if sig1.times[0]<sig2.times[0]:
        x = sig1
        y = sig2
    else:
        x = sig2
        y = sig1
    dtx = x.times[1]-x.times[0]
    dty = y.times[1]-y.times[0]
    if not Compare(dtx, dty): raise Exception("sample_periods don't match")
    flt = ((y.times[0]-x.times[0])/x.sampling_period)
    fbo = round(flt)
    if not Compare(flt, fbo): raise Exception("sample times not match. {0} and {1}, diff={2}".format(fbo, flt, fbo - flt))
    t_start = x.times[0]
    t = x.times < y.times[0]
    dist = int((y.times[0]-x.times[-1])/x.sampling_period) - 1
    ydata = y.rescale(x.units)
    if dist>0: data = np.concatenate((x.magnitude[t], np.array([0.]*dist), ydata.magnitude))
    else: data = np.concatenate((x.magnitude[t], ydata.magnitude))
    return neo.AnalogSignal(data, t_start=t_start, sampling_period=x.sampling_period, units = x.units,
                            name=name, description=description)

def ConcatSequential(sig1, sig2, t_start = None, name=None, description = None):
    if name is None : name = sig1.name
    if description is None: description = sig1.description
    if t_start is None: t_start = sig1.t_start
    if Compare(sig1.sampling_period.simplified.magnitude, sig2.sampling_period.simplified.magnitude):
        units = sig1.units
        signal = np.concatenate((sig1.magnitude, sig2.rescale(units).magnitude))
        return neo.AnalogSignal(signal, name = name, t_start = t_start,
                                sampling_period = sig1.sampling_period, units = units)

def ExpandNull(sig, time):
    if time > sig.duration:
        dtime = time-sig.duration
        ty = NearestDivident(dtime, sig.sampling_period)
        length = int(ty/sig.sampling_period)
        sb = SignalBuilder(length=length, sampling_period=sig.sampling_period)
        sig2 = sb.get_constant(0*sig.units)
        return ConcatSequential(sig, sig2)
    else: return sig

def Join(lst, name=None, description=None):
    an = lst[0]
    for k in lst[1:]:
        an = Concat(an, k)
    an.name=name
    an.description=description
    return an

def Join_Shifted(lst, dtime = 0*q.s, name=None, description=None):
    an = lst[0]
    dtime = NearestDivident(dtime, an.sampling_period)
    for i in xrange(1, len(lst)):
        an = Concat(an, ShiftSignal(lst[i], dtime*i))
    an.name=name
    an.description=description
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