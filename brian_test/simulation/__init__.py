from sig_proc import  signals as ss, plot as plt, multiple as mpl
import brian as b

class Simulator(object):
    def __init__(self, model):
        self.model = model
        eqs = model.get_model()
        thr = model.get_threshold()
        reset = model.get_reset()
        self.g = b.NeuronGroup(1, model=eqs, threshold=thr, reset=reset, method="RK")

    def set_input(self, name, input):
        signal = ss.TimedArray_from_AnalogSignal(input)
        self.model.update_inits({name: signal})

    def run(self, time=200*b.ms, dtime = 0.02*b.ms, inits={}, monitors=None):
        b.defaultclock.dt = dtime
        self.model.set_start_params(self.g, **inits)
        self.model.simulate(time, self.g, d=monitors)
        dii = self.model.return_results()
        for k in dii:
            print k, str(dii[k])
        di = self.model.return_signal()
        print di
        mpl.PlotSets(di)