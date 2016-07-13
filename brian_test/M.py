from M_base import *
from hodgkin_huxley import *
from AdEx import *

class DummyModel(model_template):
    def __init__(self):
        self.params = {}
        self.equations = ["dV/dt = 1*mV/ms : mV"]
        self.monitors_list = ['V']

