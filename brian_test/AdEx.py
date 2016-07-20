from M_base import *

class AdEx(model_template):
    def __init__(self, inits={}):
        self.opt_params = {
            "Vr":[-60., -60., -30., -29., mV],
            "Vt":[-70., -69., -40., -39., mV],
            "b": [0.001, 0.002, 0.2, 0.201, nA],
            "sF": [0.99, 1., 2.99, 3., mV],
            "tau": [10, 15, 55, 60, ms],
            "EL": [-80., -79., -60., -59., mV],
            "gL": [1., 1.1, 100., 120., nS],
            "C": [50, 60, 500, 530, pF],
            "a": [1., 1.1, 20., 22., nS]
        }
        self.def_inits = {
            "w":0*uA,
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
        self.params = {}
#            "Vr":-48.5*mV,
#            "Vt":-50.4*mV,
#            "b": 0.08 * nA,
#            "sF": 2 * mV,
#            "tau": 40 * ms,
#            "EL": -70.6 * mV,
#            "gL": 30 * nS,
#            "C": 281 * pF,
#            "a": 4 * nS
#         }
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
        tm = self.def_inits["C"]/self.def_inits["gL"]
        aa = self.def_inits["a"]/self.def_inits["gL"]
        print "C/gL", tm
        print "a/gL", aa
        print "tm/tw", tm/self.def_inits["tau"]
        self._threshold = 'V > Vt+5*sF'
        self._reset = 'V = Vr; w+=b'