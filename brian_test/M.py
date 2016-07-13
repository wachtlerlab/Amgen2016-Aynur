from M_base import *
from hodgkin_huxley import *

class DummyModel(model_template):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']

class AdEx(model_template):
    def __init__(self):
        self.def_inits = {
            "w":0*uA,
            "V":0*uA,
            "Vr":-48.5*mV,
            "Vt":-50.4*mV,
            "b": 0.08 * nA,
            "V":-70.4*mV,
            "sF": 2 * mV
        }
        self.monitors_list = {"V": mV, "I": nA, "w":nA}
        self.equations = [
            "dV/dt = (I + IL + Ex - w)/C : mV",

            "dw/dt = (a*(V - EL) - w)/tau : mA",
            "Ex = gL*sF*exp((V - Vt)/sF) : mA",
            "IL = gL*(EL - V) : mA",
            "dI/dt = cI : mA",
            "DV : mV",
            "Vt : mV",
            "Vr : mV",
            "b : mA",
            "sF : mV",
            ""
        ]
        self.params = {
            "tau": 40 * ms,
            "EL": -70.6 * mV,
            "gL": 30 * nS,
            "C": 281 * pF,
            "a": 4 * nS,
            "cI": 0*mA/ms,
            }
        self._threshold = 'V > Vt + 5*sF'
        self._reset = 'V = Vr; w+=b'

