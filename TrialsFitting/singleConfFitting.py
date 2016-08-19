from NixUtils.NixModelFitter import NixModelFitter
from BrianUtils.NeuronModels import AdEx
from datetime import datetime
from NixUtils import ProjectFileStructure as fs
import os
import sys
import ast

#print sys.argv

task = ast.literal_eval(sys.argv[1])
#print task

neuron = str(task["neuron"])
nixMF = NixModelFitter(neuron)
model = str(task["model"])
regime = str(task["regime"])
iters = int(task["iters"])
optparams = map(str, task["optparams"])
algoptparams = {"proportion_selective": 0.5}
output = str(task["output"])
input = str(task["input"])

inits = getattr(AdEx.AdEx, regime)

t = datetime.now()
logstr = "Fitting started at "+ str(t) + "\n"
logstr = "Neuron: "+neuron+"\n"
logstr += "Model: " + model + "\n"
logstr += "Initial point: " + str(regime) + "\n"
logstr += "Optimized parameters: " + str(optparams) + "\n"
logstr += "Iterations: " + str(iters) + "\n"
logstr += "Algorithm parameters: " + str(algoptparams) + "\n"

print "///---------------///"
print logstr

res = nixMF.FitModel(model, input=input,
                     output=output, maxiter=iters,
                     inits=inits, algoptparams=algoptparams, from_perc=False,
                     popsize=1000, optparams=optparams, returninfo=True)

t = datetime.now()
logstr += "Finished at " + str(t) + "\n"
logstr += "Fitting name: " + str(res) + "\n"
confname = task["file"]
if not logstr is None:
    logfile = open(os.path.join(fs.OUTPUT, confname + "__" + res + ".log"), "w")
    logfile.write(logstr)
    logfile.close()