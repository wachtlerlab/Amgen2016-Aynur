from M_base import *

class hodgkin_huxley(model_template):
    def __init__(self):
        self.def_inits = {"n":0.31, "m":0.05, "h": 0.6}
        self.monitors_list = {"V":mV, "INa":10*uA, "IK":10*uA, "Il":10*uA, "I":10*uA}
        self.equations = [
                "dV/dt = (I + INa + IK + Il)/C : mV",

                "INa = gNa*m**3*h*(ENa-V) : mA",
                "IK = gK*n**4*(EK-V) : mA",
                "Il = gl*(El-V) : mA",

                "dn/dt = (an*(1-n)-bn*n)/tau2 : 1",
                "an = n_a_A*(VD-n_a_B)/(exp((VD-n_a_B)/n_a_C)-n_a_D) : 1",
                "bn = n_b_A*exp(VD/n_b_C) : 1",

                "dm/dt = (am*(1-m)-bm*m)/tau2 : 1",
                "am = m_a_A*(VD-m_a_B)/(exp((VD-m_a_B)/m_a_C)-m_a_D) : 1",
                "bm = m_b_A*exp(VD/m_b_C) : 1",

                "dh/dt = (ah*(1-h)-bh*h)/tau2 : 1",
                "ah = h_a_A*exp(VD/h_a_C) : 1",
                "bh = h_b_A/(exp((VD-h_b_B)/h_b_C)-h_b_D) : 1",
                "dI/dt = -I/tau : mA",
                "VD = V - Vr : mV"
                ]
        self.params = {
            "tau": 0.2*ms,
            "tau2": 1.*ms,
            "ENa": -115.*mV,
            "EK": 12.*mV,
            "El": -10.613*mV,
            "gl": 0.3*msiemens,
            "gK": 36.0*msiemens,
            "gNa": 120.0*msiemens,
            "Vr": 0.*mV,
            "C": 1.*ufarad,
            "n": {  "a": {
                        "A": 0.01/mV,
                        "B": -10.0*mV,
                        "C": 10.0*mV,
                        "D": 1.0 },
                    "b": {
                        "A": 0.125,
                        "C": 80.0*mV }
                },
            "m": {  "a": {
                        "A": 0.1/mV,
                        "B": -25.0*mV,
                        "C": 10.0*mV,
                        "D": 1.0 },
                    "b": {
                        "A": 4.0,
                        "C": 18.0*mV }
                },
            "h": {  "a": {
                        "A": 0.07,
                        "C": 20.0*mV },
                    "b": {
                        "A": 1.,
                        "B": -30.0*mV,
                        "C": 10.0*mV,
                        "D": -1.0 }
                }
            }
