from BrianUtils.Utilities import timer
t = timer()
import sys
from NixUtils import ModelfittingIO as mio
from Storage import ProjectStructure as pstr
from NeoUtils.NeoPlot import NeoPlotter

def printlst(lst):
    for i in xrange(len(lst)):
        print i, ": ", lst[i]

expname = pstr.getSettings()["expname"]

np = NeoPlotter()
m = sys.argv[1:]
f = mio.ModelfittingIO(expname, pstr.FITTING)
inputs = f.GetInNames()
outputs = f.GetOutNames()

colorgroup = None
legend = True
xlabel = None
ylabel = None

for ko in m:
    k = ko.split(":")
    if k[0]=="inp":
        res = f.GetIn(inputs[int(k[1])])
        np.PlotSignal(res, colorgroup=colorgroup)
    elif k[0]=="out":
        res = f.GetOut(outputs[int(k[2])])
        if k[1][0]=="+": np.PlotSignal(res[0], colorgroup=colorgroup)
        if k[1][1]=="+": np.PlotSpiketrain(res[1], colorgroup=colorgroup)
    elif k[0]=="col":
        colorgroup = int(k[1])
    elif k[0]=="sub":
        np.Subplot(int(k[1][0]), int(k[1][1]), int(k[1][2]),"", legend, xlabel=xlabel, ylabel=ylabel)
    elif k[0]=="tit":
        np.Title(k[1])
    elif k[0]=="leg":
        if k[1]=="1":
            legend = True
        else: legend = False
    elif k[0]=="xlab":
        np.Xlabel(k[1])
        xlabel = k[1]
    elif k[0]=="ylab":
        np.Ylabel(k[1])
        ylabel = k[1]
    elif k[0]=="list":
        if k[1]=="i":
            print "Inputs: "
            printlst(inputs)
        elif k[1]=="o":
            print "Outputs: "
            printlst(outputs)
    elif k[0]=="show":np.Show()