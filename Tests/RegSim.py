from NixUtils import NixModelFitter as NF
from BrianUtils.NeuronModels import AdEx
from matplotlib import pylab as plt
import os
import numpy as np
import sys


expname = sys.argv[1]
predirec = sys.argv[2]

direc = os.path.join(predirec, expname)

if not os.path.exists(direc):
    os.mkdir(direc)

f = NF.NixModelFitter(expname, mode="r")
lst = f.GetFittingNames()

func1 = lambda x: x
func2 = lambda x: 0.25 * x * (1 - (1 / x)) ** 2

pos = 1
for i in map(int, sys.argv[3:]):
    print lst[i]
    g = f.file.GetFit(lst[i])
    inits = g["inits"]
    print inits
    fitted = inits.copy()
    fitted.update(g["fitted"])
    if g["model"]=="adex":
        plt.figure(figsize=(16, 12))
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
        filename1 = os.path.join(direc, lst[i]+"_REG.png")
        plt.savefig(filename1)
        sigfilter = lambda x: True if x.description == "from the model" and x.name != "w" else False
        filename2 = os.path.join(direc, lst[i]+"_SIM.png")
        f.SimulateAndPlotFitting(lst[i], legend=True, sigfilter=sigfilter, savesize=(24, 18), savename=filename2)
    else:
        print "Model {0} is not AdEx model".format(g["model"])