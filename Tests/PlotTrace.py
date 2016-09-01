'''
Simple-to-use script to visualize data in NIX file.

Usage:

python Test/PlotTrace.py command1[:param1] command2[:param2]

Example:

python Test/PlotTrace.py list:i list:o inp:0 out+-:3 show

It'll list inputs available, then outputs available, then will plot input with number 0
and output with number 3 (only analogsignal, not spiketrain),
and finally show it on the screen.

python Tests/PlotTrace.py sub:121 xlab:'time, ms' ylab:'Nice axis' col:0 inp:0 out++:0 col:1 inp:4 out+-:2 leg:0 save:superplot.png

Will plot input 0 and output 0 (both signal and spiketrain) in one color,
input 4 and output 2(without spiketrain) - in other,
on the subplot 121 (width height pos), with xlabel='time, ms' and ylabel='Nice axis'
without legend
and save plot as png with filename superplot.png
'''
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
    elif k[0][:3]=="out":
        res = f.GetOut(outputs[int(k[1])])
        if k[0][3]=="+": np.PlotSignal(res[0], colorgroup=colorgroup)
        if k[0][4]=="+": np.PlotSpiketrain(res[1], colorgroup=colorgroup)
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
    elif k[0]=="save":np.Show(filename=k[1])