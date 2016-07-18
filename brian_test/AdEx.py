from M_base import *

class AdEx(model_template):
    def __init__(self, inits={}):
        self.def_inits = {
            "w":0*uA,
            "V":0*uA,
            "Vr":-48.5*mV,
            "Vt":-50.4*mV,
            "b": 0.08 * nA,
            "V":-70.4*mV,
            "sF": 2 * mV,
            "tau": 40 * ms,
            "EL": -70.6 * mV,
            "gL": 30 * nS,
            "C": 281 * pF,
            "a": 4 * nS
        }
        self.def_inits.update(inits)
        self.monitors_list = {"V": mV, "I": nA, "w":0.1*nA}
        self.equations = [
            "dV/dt = (I + IL + Ex - w)/C : mV",

            "dw/dt = (a*(V - EL) - w)/tau : mA",
            "Ex = gL*sF*exp((V - Vt)/sF) : mA",
            "IL = gL*(EL - V) : mA",
            "I : mA",
            "Vt : mV",
            "Vr : mV",
            "b : mA",
            "sF : mV",
            "tau: ms",
            "EL : mV",
            "gL : siemens",
            "C : pF",
            "a : siemens"
            ""
        ]
        self.params = {}
        tm = self.def_inits["C"]/self.def_inits["gL"]
        aa = self.def_inits["a"]/self.def_inits["gL"]
        print "C/gL", tm
        print "a/gL", aa
        print "tm/tw", tm/self.def_inits["tau"]
        self._threshold = 'V > Vt'
        self._reset = 'V = Vr; w+=b'