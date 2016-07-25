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

