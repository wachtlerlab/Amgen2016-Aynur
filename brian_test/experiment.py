import fitSomeModel as fm
import single_cell_test as sst
from brian_test.NeuronModels import M
from nix_utilities import XtractDataFromExp as xt


class input_signal(xt.Foo):
    def __init__(self, name, x, y):
        self.signal = y
        self.times = x
        self.var = name

exp = "130322-1LY"#raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'

data = xt.getDataFromExp(exp)
#pe.plotData(data)
rec = [f for f in data.RAW if f.name=="fitting"][0]
print rec.x
input = input_signal("I", rec.x, rec.y * M.nA / M.mV)

preout = [list(f.times*f.units) for f in data.SPIKES][:2]
if len(preout)>0:
    output_list = [zip([i]*len(preout[i]), preout[i]) for i in range(len(preout))]
    output = []
    for i in output_list: output+=i
    print output
    fit, time = fm.FitModel(M.AdEx(), input, output, maxiter=2, popsize=100)
    print "Fitting time: ",time
    print "Fitting info: ",fit.info
    data.FIT = []
    for i in range(len(preout)):
        di = fit.best_pos[i]
        di.update({"I": M.TimedArray(input.signal, input.times)})
        start = input.times[0]
        end = input.times[-1]
        dtime = 0.5*(end-start)/(len(input.times)-1)
        print "Time step: ", dtime
        ndata_d = sst.return_custom_single_test(M.AdEx, di, start, end, dtime)
        for j in ndata_d:
            ndata = ndata_d.get(j)
            if ndata!=None:
                ndata.name = data.SPIKES[i].name
                data.FIT.append(ndata)
    xt.plotData(data)