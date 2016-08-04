from Models import ModelTemplate
from brian import mV, mA, uA, nA, ms, uS, nS, uF, nF, pF

class Izhikevich(ModelTemplate):
    name = "Izhikevich model"
    id = "izhi"
    def __init__(self, inits={}):
        self.params = {}
        self.def_inits = {
            "U":0*uA,
            "V":0*uA,
            "a":0.02/ms,
            "b":0.2,
            "c":-65*mV,
            "d":2*mV
        }
        self.def_inits.update(inits)
        self.monitors_list = {"V": mV, "U": mV, "I":mA}
        self.equations = [
            "dV/dt = 140*mV/ms + 5*V/ms + 0.04*V**2/mV/ms + i*mV/mA/ms - U/ms : mV",
            "dU/dt = a*(b*V - U) : mV",
            "a : 1/ms",
            "b : 1",
            "c : mV",
            "d : mV"
        ]
        self._threshold = 'V > 30*mV'
        self._reset = 'V = c; U+=d'