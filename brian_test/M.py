from brian import *
import json_to_one_lauer as JL

class Dmodel:

    def __init__(self):
        self.equations = []
        self.params = {}
        self.def_inits = {}
    	pass

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
        for k in d:
            self.monitors[k] = StateMonitor(g, k, record=[0])
        run(time, threads=2)
        return self.monitors

    def set_start_params(self, g, **kwargs):
        init = self.def_inits.copy()
        init.update(kwargs)
        for k in init:
            setattr(g, k, init[k])

    def plot_results(self):
        print "times:|",self.monitors['V'].times, "|"
        for i in self.monitors:
            plot(self.monitors[i].times / ms, self.monitors[i][0] / mvolt, label=i)
        legend()
        show()

class DummyModel(Dmodel):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']


class hodjkin_huxley(Dmodel):
    def __init__(self):
        self.def_inits = {"n":0., "m":0., "h": 0.6}
        self.monitors_list = ["V","bm", "bn", "bh", "KK"]
        self.equations = [
                "dV/dt = 1*mV/tau2 : mV",#(I + INa + IK + Il)/C : mvolt",

                "INa = gNa*m**3*h*(ENa-V) : mA",
                "IK = gK*n**4*(EK-V) : mA",
                "Il = gl*(El-V) : mA",

                "dn/dt = (an*(1-n)+bn*n)/tau2 : 1",
                "an = n_a_A*(V-Vr-n_a_B)/(exp((V-Vr-n_a_B)/n_a_C)-n_a_D) : 1",
                "bn = n_b_A*exp((V-Vr)/n_b_C) : 1",

                "dm/dt = (am*(1-m)+bm*m)/tau2 : 1",
                "am = m_a_A*(V-Vr-m_a_B)/(exp((V-Vr-m_a_B)/m_a_C)-m_a_D) : 1",
                "bm = m_b_A*exp((V-Vr)/m_b_C) : 1",

                "dh/dt = (ah*(1-h)+bh*h)/tau2 : 1",
                "bh = h_b_A/(exp((V-Vr-h_b_B)/h_b_C)-h_b_D) : 1",
                "ah = h_a_A*exp((V-Vr)/h_a_C) : 1",
                "dI/dt = -I/tau : mA",
                "KK = V-Vr : mV"
                ]

        self.params = {
            "tau": 1*msecond,
            "tau2": 8*msecond,
            "ENa": 70*mvolt,
            "EK": -70*mvolt,
            "El": 0*mvolt,
            "gl": 0.001*siemens,
            "gK": 1.0*siemens,
            "gNa": 1.0*siemens,
            "Vr": -65*mvolt,
            "C": 1*ufarad,
            "n": {
                "a": {
                    "A": 0.01/mvolt,
                    "B": -10.0*mvolt,
                    "C": 10.0*mvolt,
                    "D": 1.0
                },
                "b": {
                    "A": 0.125,
                    "C": 80.0*mvolt
                }
            },
            "m": {
                "a": {
                    "A": 0.1/mvolt,
                    "B": -25.0*mvolt,
                    "C": 10.0*mvolt,
                    "D": 1.0
                },
                "b": {
                    "A": 4.0,
                    "C": 18.0*mvolt
                }
            },
            "h": {
                "a": {
                    "A": 0.07,
                    "C": 20.0*mvolt
                },
                "b": {
                    "A": 1,
                    "B": -30.0*mvolt,
                    "C": 10.0*mvolt,
                    "D": -1.0
                }
            }
        }
