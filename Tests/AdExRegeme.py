from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as fs
import sys
from matplotlib import pylab as plt
import numpy as np

n = -1 if len(sys.argv)<2 else int(sys.argv[1])

expname = "130322-1LY"

f = mio.ModelfittingIO(expname,fs.FITTING)

lst = f.GetFitNames()

print lst[n]

if lst:
    g = f.GetFit(lst[n])
    inits = g["inits"]
    print inits
    fitted = inits.copy()
    fitted.update(g["fitted"])
    if g["model"]=="adex":
        tw = inits["tau"]
        tm = inits["C"]/inits["gL"]
        f2 = inits["a"] / inits["gL"]
        f1 = tm / tw
        print "Initially: a/gL = {0}, tm/tw = {1}".format(f2, f1)
        f_tw = fitted["tau"]
        f_tm = fitted["C"]/fitted["gL"]
        f_f2 = fitted["a"] / fitted["gL"]
        f_f1 = f_tm / f_tw
        print "Fitted: a/gL = {0}, tm/tw = {1}".format(f_f2, f_f1)
        xmax = max(f1 * 2, 2, f_f1*2)
        xmin = 0.05
        x = np.arange(xmin, xmax, 0.01)
        func1 = lambda x:x
        func2 = lambda x:0.25*x*(1-(1/x))**2
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
        plt.title("Regeme for modelfitting {0}, neuron {1}".format(lst[n], expname))
        plt.xlabel("$\\tau_m / \\tau_w$")
        plt.ylabel("$a / g_L$")
        plt.legend()
        plt.show()
    else:
        print "Model {0} is not AdEx model".format(g["model"])