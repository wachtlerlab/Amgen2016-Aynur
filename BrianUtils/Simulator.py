import brian as b

from BrianUtils import NeuronModels as NM
from NeoUtils import Signals as ss


class Simulator(object):
    '''
    Class provides functions to simulate given single-compartmental model in one cell and return results
    Allows use neo.AnalogSignal
    '''
    def __init__(self, model):
        '''
        Initializes new Simulator instance.
        :param model: string, id of model you want to use. adex, hohu, izhi
        '''
        self.model = NM.GetModelById(str(model))()

    def set_input(self, name, input):
        '''
        Set input analogsignal
        :param name: variable in model you want give input to
        :param input: neo.AnalogSignal
        :return:
        '''
        signal = ss.TimedArray_from_AnalogSignal(input)
        self.model.update_inits({name: signal})

    def set_time(self, starttime):
        '''
        Sets start time for simulation
        :param starttime:
        :return:
        '''
        b.defaultclock.t = starttime

    def run(self, time=200*b.ms, dtime = 0.02*b.ms, inits={}, templ = None, monitors=None):
        '''
        Runs simulation.
        :param time: brian.second, duration of simulation
        :param dtime: brian.second, delta-time for simulation procedure
        :param inits: dict, initial parameters for model
        :param templ: string, template for initial parameters (implemented in each model class)
        :param monitors: dict {key: brian.Units} : monitors you want to use
        :return: list of neo.AnalogSignal, recordings of variable's state
        '''
        b.defaultclock.dt = dtime
        eqs = self.model.get_model()
        thr = self.model.get_threshold()
        reset = self.model.get_reset()
        if not templ is None:
            i = self.model.get_init_template(templ)
            i.update(inits)
            inits = i
        self.afterInits = inits
        self.g = b.NeuronGroup(1, model=eqs, threshold=thr, reset=reset, method="RK", clock=b.defaultclock)
        self.model.simulate(time, self.g, monitors=monitors, **inits)
        sigs = self.model.return_signal()
        spks = self.model.return_spikes()
        self.results = [sigs, spks]
        return self.results[0]