import pandas as pd
from NixUtils import ModelfittingIO as mio
from Storage import ProjectFileStructure as fs
import sys, os, json
import datetime as dt
import numpy as np

df0 = pd.DataFrame()

nixFilesFolder = sys.argv[1]
if nixFilesFolder== ":": nixFilesFolder = fs.FITTING
for configName in sys.argv[2:]:
    config = json.load(open(configName))
    confID = os.path.basename(configName)
    dirFiles = os.listdir(fs.OUTPUT)
    for i in dirFiles:
        if confID == i[:len(confID)]:
            print "LogFile", i
            stri = open(os.path.join(fs.OUTPUT, i)).read()
            di = {k[0]:k[1][1:] for k in map(lambda x:x.split(":", 1), [l for l in stri.split("\n") if ":" in l])}
            expname = di["Neuron"]
            fname = di["Fitting name"]
            f = mio.ModelfittingIO(expname, nixFilesFolder)
            fit = f.GetFit(fname)
            f.closeNixFile()
            params = fit["fitted"]
            params["neuron"] = expname
            params["input"] = fit["input"]
            params["output"] = fit["output"]
            params["model"] = fit["model"]
            params["fitting"] = fname
            params["start"] = di["Initial point"]
            params["Gamma"] = fit["Gamma"]

            df0 = df0.append(pd.DataFrame(data = params, index=[df0.shape[0]]))

young = set(["130523-3LY", "130605-1LY", "130605-2LY", "140813-3Al", "140917-1Al", "140930-1Al", "141030-1Al"])

df0["group"] = df0["neuron"].apply(lambda x:"young" if x in young else "forager")

# print df0.head()

dmax = pd.DataFrame()

for k, s in df0.groupby("neuron"):
    dd = s.fillna(0.)
    dd = dd[dd["Gamma"] <= 1.]
    n = dd["Gamma"].idxmax()
    if not np.isnan(n):
        dmax = dmax.append(s.loc[[n]])

print dmax

name = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")
df0.to_csv(os.path.join(fs.tables, name+"_FULL.csv"))
dmax.to_csv(os.path.join(fs.tables, name+".csv"))