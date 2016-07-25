import neo
import brian as b

def TimedArray_from_AnalogSignal(sig):
    return b.TimedArray(arr = sig.magnitude, times = sig.times)

def ShiftSignal(sig, dtime):
    return neo.AnalogSignal(sig.magnitude, t_start=sig.times[0]-dtime, sampling_period=sig.sampling_period, units=sig.units)

def BeginSignalOn(sig, time):
    return neo.AnalogSignal(sig.magnitude, t_start=time, sampling_period = sig.sampling_period, units = sig.units)

def ReInit(magnitude, t_start, sampling_period, units):
    return neo.AnalogSignal(magnitude, t_start=t_start, sampling_period=sampling_period, units=units)

def ShiftSpikeTrain(spk, dtime):
    return neo.SpikeTrain(spk.times - dtime, spk.t_stop-dtime, spk.units)