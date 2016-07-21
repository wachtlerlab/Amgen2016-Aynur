from brian import *
import json_to_one_lauer as JL
import numpy as np

class Foo(object):
    def __init__(self, name, x, y, xunit, yunit):
        self.name = name
        self.x = x
        self.y = y
        self.xunit = xunit
        self.yunit = yunit

class model_template:

    _threshold = None
    _reset = None
    def __init__(self):
        self.equations = []
        self.params = {}
        self.def_inits = {}
        self.opt_params = {}
    	pass

    def get_inits(self):
        return self.def_inits

    def get_opt_params(self):
        return {k: np.array(self.opt_params[k][:-1], dtype=float)*self.opt_params[k][-1] for k in self.opt_params}

    def get_params(self):
        return self.params

    def get_threshold(self):
        return self._threshold

    def get_reset(self):
        return self._reset

    def get_model(self):
        new_dic = {}
        JL.fromdict("", self.params, new_dic)
        print new_dic
        model = Equations("\n".join(self.equations), **new_dic)
        #for i in new_dic:
        #    model.substitute(i, str(new_dic[i]))
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
        init.update(kwargs)
        for k in init:
            setattr(g, k, init[k])

    def return_results(self):
        for i in self.monitors:
            unit = self.monitors_un[i]
            return Foo("Nothing", self.monitors[i].times, self.monitors[i][0], ms, unit)

    def plot_results(self, prefix=""):
        if len(self.monitors)>0:
            print "times:|",self.monitors[self.monitors.keys()[0]].times, "|"
        for i in self.monitors:
            unit = self.monitors_un[i]
            plot(self.monitors[i].times / ms, self.monitors[i][0] / unit, label="$"+prefix+i+"["+str(unit)+"]$")
#        legend()
#        show()