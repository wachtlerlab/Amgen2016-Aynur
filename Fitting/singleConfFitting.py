'''
Makes single fitting. Called by confFitting.py script, you don't need to use it.
'''
import ast
import os
import sys
from datetime import datetime

from BrianUtils import NeuronModels as NM
from Storage import ProjectStructure as fs
from NixUtils.NixModelFitter import NixModelFitter

task = ast.literal_eval(sys.argv[1])

neuron = str(task["neuron"])
nixMF = NixModelFitter(neuron)
modelID = str(task["model"])
regime = str(task["regime"])
iters = int(task["iters"])
optparams = map(str, task["optparams"])
algoptparams = {"proportion_selective": 0.5}
output = str(task["output"])
input = str(task["input"])
duration = task["duration"]

model = NM.GetModelById(modelID)
inits = getattr(model, regime)

t = datetime.now()
logstr = "Started at: "+ str(t) + "\n"
logstr += "Neuron: "+neuron+"\n"
logstr += "Model: " + modelID + "\n"
logstr += "Initial point: " + str(regime) + "\n"
logstr += "Optimized parameters: " + str(optparams) + "\n"
logstr += "Iterations: " + str(iters) + "\n"
logstr += "Algorithm parameters: " + str(algoptparams) + "\n"

print "///---------------///"
print logstr

res = nixMF.FitModel(modelID, input=input,
                     output=output, maxiter=iters,
                     inits=inits, algoptparams=algoptparams, from_perc=False,
                     popsize=1000, optparams=optparams, returninfo=True, duration = duration)

t = datetime.now()
logstr += "Finished at: " + str(t) + "\n"
logstr += "Fitting name: " + str(res) + "\n"
confname = task["file"]
if not logstr is None:
    logfile = open(os.path.join(fs.OUTPUT, confname + "__" + res + ".log"), "w")
    logfile.write(logstr)
    logfile.close()