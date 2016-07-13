from brian import *
import json_to_one_lauer as JL

class model_template:

    _threshold = None
    _reset = None
    def __init__(self):
        self.equations = []
        self.params = {}
        self.def_inits = {}
    	pass

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

    def plot_results(self, prefix=""):
        if len(self.monitors)>0:
            print "times:|",self.monitors[self.monitors.keys()[0]].times, "|"
        for i in self.monitors:
            unit = self.monitors_un[i]
            plot(self.monitors[i].times / ms, self.monitors[i][0] / unit, label=prefix+i)
#        legend()
#        show()