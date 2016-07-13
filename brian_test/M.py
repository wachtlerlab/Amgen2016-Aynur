from M_base import *
from hodgkin_huxley import *

class DummyModel(model_template):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']

class AdEx(model_template):
    def __init__(self):
        self._threshold = 'V<-30*mV'
        self._reset = 'V=4*mV'
        self.def_inits = {"n": 0.31, "m": 0.05, "h": 0.6}
        self.monitors_list = {"V": mV}
        self.equations = [
            "C*dV/dt = I + IL + Ex - w : mV",

            "tau*dw/dt = a*(V - EL) - w : mA",
            "Ex = gL*sF*exp((V - Vt)/sF) : mA",
            "IL = gL*(EL - V)",
            "",
            "",
            ""
        ]
        self.params = {
            "tau": 0.2 * ms,
            "tau2": 1. * ms,
            "ENa": -115. * mV,
            "EK": 12. * mV,
            "El": -10.613 * mV,
            "gl": 0.3 * msiemens,
            "gK": 36.0 * msiemens,
            "gNa": 120.0 * msiemens,
            "Vr": 0. * mV,
            "C": 1. * ufarad,
            "n": {"a": {
                "A": 0.01 / mV,
                "B": -10.0 * mV,
                "C": 10.0 * mV,
                "D": 1.0},
                "b": {
                    "A": 0.125,
                    "C": 80.0 * mV}
            },
            "m": {"a": {
                "A": 0.1 / mV,
                "B": -25.0 * mV,
                "C": 10.0 * mV,
                "D": 1.0},
                "b": {
                    "A": 4.0,
                    "C": 18.0 * mV}
            },
            "h": {"a": {
                "A": 0.07,
                "C": 20.0 * mV},
                "b": {
                    "A": 1.,
                    "B": -30.0 * mV,
                    "C": 10.0 * mV,
                    "D": -1.0}
            }
        }



