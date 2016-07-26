from brian_test.NeuronModels.model_template import *

class AdEx(model_template):
    def __init__(self, inits={}):
        self.opt_params = {
            # "Vr":[-55., -52., -45., -42., mV],
            # "Vt":[-59., -56., -45., -43., mV],
            "b": [0.01, 0.02, 0.16, 0.17, nA],
            "sF": [0.99, 1., 2.99, 3., mV],
            "tau": [130., 132., 158., 160., ms],
            # "EL": [-80., -79., -60., -59., mV],
            # "gL": [15., 17.1, 60., 62., nS],
            # "C": [200., 204., 360, 366, pF],
            # "a": [3., 3.1, 5., 5.2, nS]
        }
        self.def_inits = {
            "w":0*uA,
            "Vr": -70.6* mV,#-48.5*mV,
            "Vt":-50.4*mV,
            "b": 0.0805 * nA,
            "V":-70.4*mV,
            "sF": 2 * mV,
            "tau": 144 * ms,
            "EL": -70.6 * mV,
            "gL": 30 * nS,
            "C": 281 * pF,
            "a": 4 * nS
        }
        self.params = {
        }
        self.def_inits.update(inits)
        self.monitors_list = {"V": mV, "I": nA, "w":0.1*nA}
        self.equations = [
            "dV/dt = (i + IL + Ex - w)/C : mV",

            "dw/dt = (a*(V - EL) - w)/tau : mA",
            "Ex = gL*sF*exp((V - Vt)/sF) : mA",
            "IL = gL*(EL - V) : mA",
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
        # tm = self.def_inits["C"]/self.def_inits["gL"]
        # aa = self.def_inits["a"]/self.def_inits["gL"]
        # print "C/gL", tm
        # print "a/gL", aa
        # print "tm/tw", tm/self.def_inits["tau"]
        self._threshold = 'V > 20*mV'
        self._reset = 'V = Vr; w+=b'