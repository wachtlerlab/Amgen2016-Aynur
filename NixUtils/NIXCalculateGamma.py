import NixModelFitter as nio
import sys, os

direc = None if sys.argv[1]==":" else sys.argv[1]

for expname in sys.argv[2:]:
    print "//-------------//"
    print "//--Processing neuron:", expname
    f = nio.NixModelFitter(expname, dir=direc)
    flist = f.GetFittingNames()
    for fit in flist:
        print "----Fitting:", fit
        sigfilter = lambda x: True if x.description=="from the model" and x.name!="w" else False
        path = os.path.join(nio.FS.TRACES, fit+".png")
        f.SimulateAndPlotFitting(fit, sigfilter=sigfilter, savesize=(16, 12), savename=path, calculGamma=True)