import pandas as pd
from NixUtils import ModelfittingIO as mio
from Storage import ProjectFileStructure as fs
import sys, os

df0 = pd.DataFrame()
for stri in sys.argv[1:]:
    lst = stri.split("%")
    if lst[0][0] == ":":
        expname = os.path.basename(lst[0][1:]).split(".")[0]
        nixPath = os.path.dirname(lst[0][1:])
    else:
        expname = lst[0]
        nixPath = fs.FITTING
    f = mio.ModelfittingIO(expname, nixPath, mode=mio.nix.FileMode.ReadOnly)
    if lst[1][0]!="=":
        inta = int(lst[1])
        names = f.GetFitNames()
        fname = names[inta]
    else:
        fname = lst[1][1:]
    fit = f.GetFit(fname)
    f.closeNixFile()
    params = fit["fitted"]
    params["neuron"] = expname
    params["input"] = fit["input"]
    params["output"] = fit["output"]
    params["model"] = fit["model"]
    params["fitting"] = fname
    df0 = df0.append(pd.DataFrame(data=params, index=[0]))


print df0
