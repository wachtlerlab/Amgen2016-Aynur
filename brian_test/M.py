from M_base import *
from hodgkin_huxley import *

class DummyModel(model_template):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']

class AdEx(model_template):
    def __init__(self):
        self.def_inits = {"w":0*uA, "V":0*uA}
        self.monitors_list = {"V": mV, "I": uA, "w":uA}
        self.equations = [
            "dV/dt = (I + IL + Ex - w)/C : mV",

            "dw/dt = (a*(V - EL) - w)/tau : mA",
            "Ex = gL*sF*exp((V - Vt)/sF) : mA",
            "IL = gL*(EL - V) : mA",
            "dI/dt = cI : mA",
            "",
            ""
        ]
        self.params = {
            "tau": 40 * ms,
            "EL": 0 * mV,
            "gL": 0.003 * msiemens,
            "C": 1 * ufarad,
            "a": 4 * nS,
            "b": 0.08 * nA,
            "sF": 1 * mV,
            "cI": 0*mA/ms,
            "Vt": 30*mV,
            "Vr": 3*mV
            }
        self._threshold = 'V > %(Vt)f - 0.00001' % self.params
        self._reset = 'V = %(Vr)f;w+=%(b)f' % self.params


