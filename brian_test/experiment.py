from nix_test import plotFromExperiment as pe
import fitSomeModel as fm
import M
import single_cell_test as sst

class input_signal(pe.Foo):
    def __init__(self, name, x, y, xunit, yunit):
        self.signal = y*yunit
        self.times = x*xunit
        self.var = name

exp = raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'

data = pe.getDataFromExp(exp)
#pe.plotData(data)
rec = [f for f in data.RAW if f.name=="fitting"][0]
input = input_signal("I", rec.x, rec.y, rec.xunits, M.nA)
for rec in data.RAW[:1]:
    preout = [f for f in data.SPIKES if rec.name==f.name]
    if len(preout)>0:
        preout = preout[0]
        output = preout.times*preout.units
        fit, time = fm.FitModel(M.AdEx(), input, output, maxiter=100)
        print time
        print fit.best_pos
        di = fit.best_pos
        di.update({"I":M.TimedArray(input.signal, input.times)})
        start = input.times[0]
        end = input.times[-1]
        dtime = 0.5*(end-start)/(len(input.times)-1)
        sst.run_custom_single_test(M.AdEx, di, start, end, dtime)