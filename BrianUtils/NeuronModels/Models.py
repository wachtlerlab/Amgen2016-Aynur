import numpy as np

import quantities as q
from brian import Equations, StateMonitor, run

import BrianUtils.Utilities
from BrianUtils import Utilities as bu
from NeoUtils import Signals as ss

class ModelTemplate:
    name = ""
    _threshold = None
    _reset = None
    def __init__(self):
        self.name = "template"
        self.id = "temp"
        self.equations = []
        self.params = {}
        self.def_inits = {}
        self.opt_params = {}
        self.monitors_list = {}
    	pass

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.name

    def get_inits(self):
        return self.def_inits

    def update_inits(self, upd):
        self.def_inits.update(upd)

    def get_opt_params(self):
        res = {k: np.array(self.opt_params[k][:-1], dtype=float)*self.opt_params[k][-1] for k in self.opt_params}
        #res.update({"scaleFactor":[1e-7, 1e-6, 1e+6, 1e+7]})
        return res

    def get_params(self):
        return self.params

    def get_threshold(self):
        return self._threshold

    def get_reset(self):
        return self._reset

    def get_model(self):
        new_dic = {}
        BrianUtils.Utilities.one_layer_fromdict("", self.params, new_dic)
        model = Equations("\n".join(self.equations+["scaleFactor: 1\nI: mA\ni = scaleFactor*I : mA"]), **new_dic)
        return model

    def simulate(self, time, g, d = None):
        if d==None:
            d = self.monitors_list
        self.monitors = {}
        self.monitors_un = d
        for k in d:
            self.monitors[k] = StateMonitor(g, k, record=[0])
        run(time, threads=2)
        return self.monitors

    def set_start_params(self, g, **kwargs):
        init = self.def_inits.copy()
        init.update({"scaleFactor":1.})
        init.update(kwargs)
        for k in init:
            setattr(g, k, init[k])

    def return_signal_scaled(self):
        res = []
        for i in self.monitors:
            qq = bu.BrianToQuantity(self.monitors_un[i])
            mag = self.monitors[i][0]/self.monitors_un[i]
            unitq = q.UnitQuantity(str(qq), qq)
            times = q.s*self.monitors[i].times
            res.append(ss.AnalogSignalFromTimes(times, mag, unitq, i, "from the model"))
        return res

    def return_signal(self):
        res = []
        for i in self.monitors:
            qq = bu.BrianToQuantity(self.monitors_un[i])
            mag = self.monitors[i][0]/float(qq.magnitude)
            times = q.s*self.monitors[i].times
            res.append(ss.AnalogSignalFromTimes(times, mag, qq.units, i, "from the model"))
        return res

class DummyModel(ModelTemplate):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']


class Foo(object):
    def __init__(self, name, x, y, xunits, yunits):
        self.name = name
        self.label = name
        self.x = x
        self.y = y
        self.xunits = xunits
        self.yunits = yunits

    def __str__(self):
        return "%name: {0}; x: {1}; y: {2}%".format(self.name, self.x, self.y)

    def __unicode__(self):
        return self.__str__()
