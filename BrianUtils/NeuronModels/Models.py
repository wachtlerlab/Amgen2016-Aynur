import numpy as np

import quantities as q
from brian import Equations, StateMonitor, run

import BrianUtils.Utilities
from BrianUtils import Utilities as bu
from NeoUtils import Signals as ss

class Model:
    '''
    Parent class for all neuronal models
    '''
    name = ""
    _threshold = None
    _reset = None
    what_to_opt = set()
    perc = {}
    def __init__(self):
        self.name = "template"
        self.id = "temp"
        self.equations = []
        self.params = {}
        self.def_inits = {}
        self.opt_params = {}
        self.monitors_list = {}
        self.units = {}
    	pass

    def update_perc(self, di):
        '''
        Updates percentage dict with di dict
        :param di: dict
        :return: None
        '''
        self.perc.update(di)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.name

    def get_inits(self):
        '''
        Returns initial values for this model, defined so far
        :return: dict
        '''
        return self.def_inits

    def update_inits(self, upd):
        '''
        Updates inits with given dict
        :param upd: dict
        :return: None
        '''
        self.def_inits.update(upd)

    def get_optparams_dict(self):
        '''
        Gives parameters from model and their limits for optimization.
        Only used for modelfitting
        :return: dict {key : [left, right]}
        '''
        res = {k: np.array(self.opt_params[k][:-1], dtype=float)*self.opt_params[k][-1]
                    for k in self.opt_params if k in self.what_to_opt}
        # res.update({"scaleFactor":[1e-7, 1e-6, 1e+6, 1e+7]})
        return res

    def get_optparams_list(self):
        return self.what_to_opt

    def add_optparams_list(self, *params):
        '''
        Updates optimization parameter for fitting
        :param params: names of parameters, list of string
        :return: None
        '''
        self.what_to_opt.update(set(params))

    def set_optparams_list(self, *params):
        '''
        Reset optimization parameters with new values.
        :param params: list of string
        :return: None
        '''
        self.what_to_opt = (set(params)).copy()

    def calc_opt_from_perc(self):
        '''
        Calculates limits for optimization parameters from percentages
        :return: None
        '''
        self.opt_params = {}
        for k in self.what_to_opt:
            init = self.def_inits[k]
            f1 = (1-self.perc[k])*init
            f2 = (1+self.perc[k])*init
            self.opt_params[k] = [min(f1, f2), max(f1, f2), init/float(init)]

    def update_optparams_dict(self, newopt):
        '''
        Updates limits of optimization parameters with givan dict
        :param newopt: dict {key: [float left, float right, brian.Units]}
        :return: None
        '''
        self.opt_params.update(newopt)

    def get_params(self):
        '''
        Depricated. Do not use.
        :return: ~
        '''
        return self.params

    def get_threshold(self):
        '''
        Returns threshold condition for model
        :return: string
        '''
        return self._threshold

    def get_reset(self):
        '''
        Returns reset expression for model
        :return:
        '''
        return self._reset

    def get_model(self):
        '''
        Converts BrianUtils.NeuronModel.Model to brian.Equations
        :return: brian.Equations
        '''
        new_dic = {}
        BrianUtils.Utilities.one_layer_fromdict("", self.params, new_dic)
        model = Equations("\n".join(self.equations+["scaleFactor: 1\nI: mA\ni = scaleFactor*I : mA"]), **new_dic)
        return model

    def simulate(self, time, neurongroup, monitors = None, **kwargs):
        '''
        Simulates model for given period of time and neurongruop
        :param time: brian.Quantity [second] - duration of simulation
        :param neurongroup: brian.NeuronGroup, neurons to simulate
        :param monitors: dict { key: brian.Units } - monitors to use
        :param kwargs: additional initial parameters for simulation
        :return: dict of brian.StateMonitor
        '''
        init = self.def_inits.copy()
        init.update(kwargs)
        for k in init:
            setattr(neurongroup, k, init[k])
        if monitors==None:
            monitors = self.monitors_list
        self.monitors = {}
        self.monitors_un = monitors
        for k in monitors:
            self.monitors[k] = StateMonitor(neurongroup, k, record=[0])
        run(time, threads=2)
        return self.monitors

    def return_signal_scaled(self):
        '''
        Do not use!
        :return:
        '''
        res = []
        for i in self.monitors:
            qq = bu.BrianToQuantity(self.monitors_un[i])
            mag = self.monitors[i][0]/self.monitors_un[i]
            unitq = q.UnitQuantity(str(qq), qq)
            times = q.s*self.monitors[i].times
            res.append(ss.AnalogSignalFromTimes(times, mag, unitq, i, "from the model"))
        return res

    def return_signal(self):
        '''
        Returns monitored values for last simulation as list of analogsignals
        :return: list of neo.AnalogSignal
        '''
        res = []
        for i in self.monitors:
            qq = bu.BrianToQuantity(self.monitors_un[i])
            mag = self.monitors[i][0]/float(qq.units.simplified.magnitude)
            times = q.s*self.monitors[i].times
            res.append(ss.AnalogSignalFromTimes(times, mag, qq.units, i, "from the model"))
        return res


class DummyModel(Model):
    '''
    Just to check how simulation works
    '''
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']

    def __str__(self):
        return "%name: {0}; x: {1}; y: {2}%".format(self.name, self.x, self.y)

    def __unicode__(self):
        return self.__str__()
