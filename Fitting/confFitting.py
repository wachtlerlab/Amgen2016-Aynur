import json
import os
import subprocess
import sys

from Storage import ProjectFileStructure as fs
from checkConfFitting import checkConfFitting

for filename in sys.argv[1:]:
    conf = json.load(open(filename))
    for task in conf["tasks"]:
        for neuron in task["neurons"]:
            for regime in task["regimes"]:
                tsk = {
                    "input": str(task["input"]), "output": str(task["output"]),
                    "neuron": str(neuron), "regime": str(regime), "duration":task["duration"],
                    "optparams": task["optparams"], "iters": task["iters"],
                    "model": str(task["model"]), "file": os.path.basename(filename)}
                checkConfFitting(tsk)


for filename in sys.argv[1:]:
    conf = json.load(open(filename))
    for task in conf["tasks"]:
        for neuron in task["neurons"]:
            for regime in task["regimes"]:
                tsk = {
                    "input":str(task["input"]), "output":str(task["output"]),
                    "neuron":str(neuron), "regime":str(regime), "duration":task["duration"],
                    "optparams":task["optparams"], "iters":task["iters"],
                    "model":str(task["model"]), "file":os.path.basename(filename)}
                subprocess.call(["python", os.path.join(fs.scripts, "Fitting", "singleConfFitting.py"), str(tsk)])