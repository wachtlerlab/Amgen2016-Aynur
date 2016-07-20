from nix_test import plotFromExperiment as pe
import fitSomeModel as fm
import M
import quantities as q

class input_signal(pe.Foo):
    def __init__(self, name, x, y, xunit, yunit):
        self.signal = y*yunit
        self.times = x*xunit
        self.var = name

exp = ""  # "= raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'

data = pe.getDataFromExp(exp)
#pe.plotData(data)
rec = [f for f in data.RAW if f.name=="fitting"][0]
input = input_signal("I", rec.x, rec.y, rec.xunits, q.nA)
for rec in data.RAW:
    preout = [f for f in data.SPIKES if rec.name==f.name]
    if len(preout)>0:
        preout = preout[0]
        output = preout.times*preout.units
        fit = fm.FitModel(M.AdEx(), input, output, cpu=None, gpu=None)