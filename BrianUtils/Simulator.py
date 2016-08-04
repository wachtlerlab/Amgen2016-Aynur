import brian as b

from NeoUtils import Signals as ss


class Simulator(object):
    def __init__(self, model):
        self.model = model

    def set_input(self, name, input):
        signal = ss.TimedArray_from_AnalogSignal(input)
        self.model.update_inits({name: signal})

    def set_time(self, time):
        b.defaultclock.t = time

    def run(self, time=200*b.ms, dtime = 0.02*b.ms, inits={}, monitors=None):
        b.defaultclock.dt = dtime
        eqs = self.model.get_model()
        thr = self.model.get_threshold()
        reset = self.model.get_reset()
        self.g = b.NeuronGroup(1, model=eqs, threshold=thr, reset=reset, method="RK", clock=b.defaultclock)
        self.model.set_start_params(self.g, **inits)
        self.model.simulate(time, self.g, d=monitors)
        di = self.model.return_signal()
        self.results = di
        return self.results