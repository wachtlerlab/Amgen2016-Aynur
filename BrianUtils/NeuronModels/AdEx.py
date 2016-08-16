from Models import Model
from brian import mV, mA, uA, nA, ms, uS, nS, uF, nF, pF

class AdEx(Model):
    '''
    Class for Adaptive Exponential Integrate-and-Fire model. Inherits from BrianUtils.NeuronModels.Models.Model
    '''
    name = "AdEx model"
    id = "adex"
    def __init__(self, inits={}, from_perc = False):
        self.opt_params = {
            "Vr":[-85., -30., mV],
            "Vt":[-56., -45., mV],
            "b": [0.0002, 4, nA],
            "sF": [0.1, 13., mV],
            "tau": [5., 1220., ms],
            "gL": [0.1, 760., nS],
            "C": [0.1, 1e3, pF],
            "scaleFactor": [1e-2, 1e+2, 1.],
            "a": [.1, 1755., nS]
        }

        self.what_to_opt = set(["Vr", "sF", "tau", "b"])

        self.def_inits = {
            "w": 0*uA,
            "Vr": -70.6 * mV,#-48.5*mV,
            "Vt":-50.4 * mV,
            "b": 0.0805 * nA,
            "V":-70.4 * mV,
            "sF": 2 * mV,
            "scaleFactor": 1.,
            "tau": 144 * ms,
            "EL": -70.6 * mV,
            "gL": 30 * nS,
            "C": 281 * pF,
            "a": 4 * nS,
            "Vp": -25 * mV
        }
        self.params = {
        }
        self.def_inits.update(inits)
        if from_perc:
            self.calc_opt_from_perc()
        self.monitors_list = {"V": mV, "I": nA, "w":0.1*nA}
        self.equations = [
            "Ex = gL*sF*exp( (V - Vt)/sF ) : mA",
            "IL = gL*(EL - V) : mA",
            "dV/dt = (i + IL + Ex - w)/C : mV",

            "dw/dt = (a*(V - EL) - w)/tau : mA",
            "Vt : mV",
            "Vr : mV",
            "b : mA",
            "sF : mV",
            "tau: ms",
            "EL : mV",
            "gL : siemens",
            "C : pF",
            "a : siemens",
            "Vp : mV"
        ]
        self._threshold = 'V > Vp'
        self._reset = 'V = Vr; w+=b'

    def get_init_template(self, stri):
        return getattr(self, stri, {})

    resonator = {
        "b": 0.0805 * nA,
        "V":-70.4*mV,
        "sF": 2 * mV,
        "tau": 144 * ms,
        "EL": -70.6 * mV,
        "gL": 20 * nS,
        "C": 2810 * pF,
        "a": 8 * nS
    }

    integrator = {
        "b": 0.0805 * nA,
        "V":-70.4*mV,
        "sF": 2 * mV,
        "tau": 144 * ms,
        "EL": -70.6 * mV,
        "gL": 20 * nS,
        "C": 12 * nF,
        "a": 4 * nS
    }

    rebound = {
        "w": 0 * uA,
        "Vr": -60 * mV,  # -48.5*mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 720 * ms,
        "EL": -60 * mV,
        "gL": 30 * nS,
        "C": 281 * pF,
        "a": 80 * nS
    }

    bursting = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -70.4 * mV,
        "sF": 2 * mV,
        "tau": 144 * ms,
        "EL": -70.6 * mV,
        "gL": 30 * nS,
        "C": 281 * pF,
        "a": 4 * nS
    }

    bursting_rebound = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 720 * ms,
        "EL": -60 * mV,
        "gL": 30 * nS,
        "C": 281 * pF,
        "a": 80 * nS
    }

    perc = {
        "Vr": 0.1,
        "Vt": 0.1,
        "b": 0.99,
        "sF": 0.2,
        "tau": 0.6,
        "gL": 0.01,
        "C": 0.2,
        "a": 0.4
    }

    hopf_resonator = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 120 * ms,
        "EL": -60 * mV,
        "gL": 30 * nS,
        "C": 681 * pF,
        "a": 80 * nS
    }

    hopf_resonator2 = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 120 * ms,
        "EL": -60 * mV,
        "gL": 6 * nS,
        "C": 1200 * pF,
        "a": 80 * nS
    }

    saddle_resonator = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 12 * ms,
        "EL": -60 * mV,
        "gL": 30 * nS,
        "C": 800 * pF,
        "a": 30 * nS
    }

    saddle_resonator2 = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 12 * ms,
        "EL": -60 * mV,
        "gL": 3 * nS,
        "C": 800 * pF,
        "a": 30 * nS
    }

    saddle_integrator = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 12 * ms,
        "EL": -60 * mV,
        "gL": 40 * nS,
        "C": 1200 * pF,
        "a": 3 * nS
    }

    saddle_mixed = {
        "w": 0 * uA,
        "Vr": -47.4 * mV,
        "Vt": -50.4 * mV,
        "b": 0.0805 * nA,
        "V": -60 * mV,
        "sF": 2 * mV,
        "tau": 12 * ms,
        "EL": -60 * mV,
        "gL": 80 * nS,
        "C": 300 * pF,
        "a": 10 * nS
    }

    result13 = {
        "w": 0 * uA,
        "Vr": -62.8 * mV,
        "Vt": -49.2 * mV,
        "b": 1.41 * nA,
        "V": -60 * mV,
        "sF": 7.2 * mV,
        "tau": 600 * ms,
        "EL": -60 * mV,
        "gL": 80 * nS,
        "C": 276 * pF,
        "a": 1037 * nS
    }

def ActType(inits):
    tw = inits["tau"]
    tm = inits["C"] / inits["gL"]
    f2 = inits["a"] / inits["gL"]
    f1 = tm / tw
    return f1, f2