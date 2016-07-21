from nix_test import XtractDataFromExp as xt
import fitSomeModel as fm
import M
import single_cell_test as sst

class input_signal(xt.Foo):
    def __init__(self, name, x, y, xunit, yunit):
        self.signal = y*yunit
        self.times = x*xunit
        self.var = name

exp = "130322-1LY"#raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'

data = xt.getDataFromExp(exp)
#pe.plotData(data)
rec = [f for f in data.RAW if f.name=="fitting"][0]
input = input_signal("I", rec.x, rec.y, rec.xunits, M.nA)

preout = [list(f.times*f.units) for f in data.SPIKES][:2]
if len(preout)>0:
    print preout
    output_list = [zip([i]*len(preout[i]), preout[i]) for i in range(len(preout))]
    output = []
    for i in output_list: output+=i
    print output
    fit, time = fm.FitModel(M.AdEx(), input, output, maxiter=2, popsize=100)
    print time
    print fit.best_pos
    print fit.info
    data.FIT = []
    for i in range(len(preout)):
        di = fit.best_pos[i]
        di.update({"I":M.TimedArray(input.signal, input.times)})
        start = input.times[0]
        end = input.times[-1]
        dtime = 0.5*(end-start)/(len(input.times)-1)
        ndata = sst.return_custom_single_test(M.AdEx, di, start, end, dtime)
        ndata.name = data.SPIKES[i].name
        data.FIT.append(ndata)
    xt.plotData(data)