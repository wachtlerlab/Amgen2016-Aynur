from BrianUtils.Utilities import timer
t = timer()
import sys
from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as pstr
from NeoUtils.NeoPlot import NeoPlotter
from NeoUtils.NeoPlot import PlotLists
from NeoUtils.NeoJsonIO import PlotJsonAnalogSignals
from NeoUtils.NeoJsonIO import SaveResults
from BrianUtils import Simulator
import datetime as dt

def printlst(lst):
    for i in xrange(len(lst)):
        print i, ": ", lst[i]

np = NeoPlotter()
m = sys.argv[1:]
f = mio.ModelfittingIO("140917-1Al", pstr.FITTING)
inputs = f.GetInNames()
outputs = f.GetOutNames()
sims = f.GetSimNames()

colorgroup = None
legend = True
xlabel = None
ylabel = None
for k in m:
    if k[0]=="i":
        res = f.GetIn(inputs[int(k[1:])])
        np.PlotSignal(res, colorgroup=colorgroup)
    elif k[0]=="o":
        res = f.GetOut(outputs[int(k[3:])])
        if k[1]=="1": np.PlotSignal(res[0], colorgroup=colorgroup)
        if k[2]=="1": np.PlotSpiketrain(res[1], colorgroup=colorgroup)
    elif k[0]=="c":
        colorgroup = int(k[1:])
    elif k[0]=="s":
        np.Subplot(int(k[1]), int(k[2]), int(k[3]),"", legend, xlabel=xlabel, ylabel=ylabel)
    elif k[0]=="t":
        np.Title(k[1:])
    elif k[0]=="l":
        if k[1]=="1":
            legend = True
        else: legend = False
    elif k[0]=="x":
        np.Xlabel(k[1:])
        xlabel = k[1:]
    elif k[0]=="y":
        np.Ylabel(k[1:])
        ylabel = k[1:]
    elif k[0]=="n":
        if k[1]=="i":
            print "Inputs: "
            printlst(inputs)
        elif k[1]=="o":
            print "Outputs: "
            printlst(outputs)
    elif k[0]=="P":np.Show()
    elif k[0]=="S":
        o = k[1:].split("/")
        model = o[0]
        sim = Simulator.Simulator(o[0])
        par = {}
        dp = {}
        in_name = ""
        out_name = outputs[-1]
        for i in o[1:]:
            a = i.split(":")
            if a[0][0] == "p":
                par[a[0][1:]] = float(a[1])
            elif a[0][0] == "i":
                if a[1][0]=="%":
                    in_name = inputs[int(a[1][1:])]
                else: in_name = a[1]
                sim.set_input(a[0][1:], f.GetIn(in_name))
            elif a[0][0] == "o":
                if a[1][0]=="%":
                    out_name = outputs[int(a[1][1:])]
                else: out_name = a[1]
            elif a[0][0] == "b":
                val = float(a[1][1:]) if a[1][0]=="%" else a[1]
                dp[a[0][1:]] = val
        start = dp.get("s")
        if not start is None: sim.set_time(start*Simulator.b.ms)
        time = dp.get("t")
        templ = dp.get("p")
        if not time is None:
            res = sim.run(time*Simulator.b.ms, inits = par, templ = templ)
        else: res = sim.run(inits = par)
        fname = str(dt.datetime.now())+"_SIM"
        filename = pstr.os.path.join(pstr.TRACES, fname)
        SaveResults(filename, res, [])
        PlotJsonAnalogSignals(filename)
        # f.AddFit(fname, model, None, sim.afterInits, in_name, out_name)
        # f.AddSim(fname, res)
        # PlotLists([zip(res, [None]*len(res))])