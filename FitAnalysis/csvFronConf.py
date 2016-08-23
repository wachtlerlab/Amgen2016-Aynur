import pandas as pd
from NixUtils import ModelfittingIO as mio
from NixPreparator import ProjectFileStructure as fs
import sys, os, json
import datetime as dt

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

            df0 = df0.append(pd.DataFrame(data = params, index=[df0.shape[0]]))

print df0.head()

name = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")

df0.to_csv(os.path.join(fs.tables, name+".csv"))