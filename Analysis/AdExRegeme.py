'''
Generates regime plot for fitting.
Only for AdEx model!

Usage:

python Analysis/AdExRegime.py -1

Plots regime plot for last fitting in current NIX file.

python Analysis/AdExRegime

Plots available fittings
'''
import sys
import numpy as np
from matplotlib import pylab as plt
from BrianUtils.NeuronModels import AdEx
from NeoUtils import NeoPlot as nep
from Storage import ProjectStructure as pstr
from NixUtils import ModelfittingIO as mio

if len(sys.argv)<2: n = None
else: n = True

expname = pstr.getSettings()["expname"]

f = mio.ModelfittingIO(expname, pstr.FITTING)

lst = f.GetFitNames()

if n is None:
    print lst

func1 = lambda x: x
func2 = lambda x: 0.25 * x * (1 - (1 / x)) ** 2

pos = 1
for i in map(int, sys.argv[1:]):
    print lst[i]
    if lst:
        g = f.GetFit(lst[i])
        inits = g["inits"]
        print inits
        fitted = inits.copy()
        fitted.update(g["fitted"])
        if g["model"]=="adex":
            nep.subplot(1, len(sys.argv)-1, pos)
            pos+=1
            f1, f2 = AdEx.ActType(inits)
            print "Initially: a/gL = {0}, tm/tw = {1}".format(f2, f1)
            f_f1, f_f2 = AdEx.ActType(fitted)
            print "Fitted: a/gL = {0}, tm/tw = {1}".format(f_f2, f_f1)
            xmax = max(f1 * 2, 2, f_f1*2)
            xmin = 0.05
            x = np.arange(xmin, xmax, 0.01)
            y1 = func1(x)
            y2 = func2(x)
            plt.plot(x, y1, label = "Hopf/Saddle-node")
            plt.plot(x, y2, label = "Resonator/Integrator")
            plabel = "Initially, "
            plabel += "Saddle-node, " if f2 < func1(f1) else "Hopf, "
            plabel += "Resonator" if f2 > func2(f1) else "Integrator" if f1 > 1 else "Mixed"
            plt.plot(f1, f2, "bo-", label=plabel)
            plabel = "After fitting, "
            plabel += "Saddle-node, " if f_f2 < func1(f_f1) else "Hopf, "
            plabel += "Resonator" if f_f2 > func2(f_f1) else "Integrator" if f_f1 > 1 else "Mixed"
            plt.plot(f_f1, f_f2, "ro-", label=plabel)
            plt.title("Regeme for modelfitting {0}, neuron {1}".format( lst[i], expname))
            plt.xlabel("$\\tau_m / \\tau_w$")
            plt.ylabel("$a / g_L$")
            plt.legend()

        else:
            print "Model {0} is not AdEx model".format(g["model"])

plt.show()