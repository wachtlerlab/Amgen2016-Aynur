import NixUtils.NixModelFitter as nio
from Storage import ProjectStructure as fs
import sys, os

direc = fs.FITTING if sys.argv[1]==":" else sys.argv[1]

if len(sys.argv[2:])>0:
    lst = sys.argv[2:]
else:
    lst = [x.split(".")[0] for x in os.listdir(direc) if ".h5" in x]

for expname in lst:
    print "//-------------//"
    print "//--Processing neuron:", expname
    f = nio.NixModelFitter(expname, dir=direc)
    flist = f.GetFittingNames()
    for fit in flist:
        print "----Fitting:", fit
        sigfilter = lambda x: True if x.description=="from the model" and x.name!="w" else False
        path = os.path.join(nio.FS.TRACES, fit+".png")
        f.SimulateAndPlotFitting(fit, sigfilter=sigfilter, savesize=(16, 12), savename=path, calculGamma=True)
