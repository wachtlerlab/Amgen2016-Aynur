from NixUtils.NixModelFitter import NixModelFitter
from BrianUtils.NeuronModels import AdEx
from datetime import datetime
from NixUtils import ProjectFileStructure as fs
import os
import sys
import ast

nixMF = NixModelFitter(task["neuron"])
nixMF = NixModelFitter(task["neuron"])
neuron = sys.argv[1]
model = sys.argv[2]
regime = sys.argv[3]
iters = int(sys.argv[4])
optparams =


t = datetime.now()
inits = getattr(AdEx.AdEx, regime)

algoptparams = {"proportion_selective": 0.5}
optparams = map(str, task["optparams"])

logstr = "Fitting started at "+ str(t) + "\n"
logstr += "Model: " + model + "\n"
logstr += "Initial point: " + str(regime) + "\n"
logstr += "Optimized parameters: " + str(optparams) + "\n"
logstr += "Iterations: " + str(iters) + "\n"
logstr += "Algorithm parameters: " + str(algoptparams) + "\n"
print "///---------------///"
print logstr
res = nixMF.FitSomething(model, input="subthreshold-DuringAfterStimulus-e-7",
                         output="Trial4-DuringAfterSimiulus", maxiter=iters,
                         inits=inits, algoptparams=algoptparams, from_perc=False,
                         popsize=1000, optparams=optparams, returninfo=True)
t = datetime.now()
logstr += "Finished at " + str(t) + "\n"
logstr += "Fitting name: " + str(res) + "\n"
confname = os.path.basename(filename)
if not logstr is None:
    logfile = open(os.path.join(fs.OUTPUT, confname + "__" + res + ".log"), "w")
    logfile.write(logstr)
    logfile.close()