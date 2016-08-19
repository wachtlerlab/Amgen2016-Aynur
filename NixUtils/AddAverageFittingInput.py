'''from matplotlib import pylab as plt
import numpy as np
import neo
import json
import nixio as nix
import neoNIXIO as nx
from quantities import Hz
import quantities as qs
import rawDataProcess as rd
import os


INFO_ABOUT_SCRIPT: "Adds subthreshold inputs for each of neuron NIX file, using parameters of double exponents from bestPars.json
                    and copies modified file into reorg directory from exp_data"



def doubleExpFun(xSig, Ar, Ad, t0, itaur, itaud):

    expd = Ad * np.exp(-itaud * (xSig - t0))
    expr = Ar * np.exp(-itaur * (xSig - t0))

    doubleExp = expd - expr
    doubleExp[xSig < t0] = (Ad - Ar)

    return doubleExp

def twoDoubleExps(xSig, A1, A2, t1, t2, taur1, taud1, taur2, taud2, offset):

        print A1, A2, t1, t2, taur1, taud1, taur2, taud2, offset

        d1 = doubleExpFun(xSig, A1, A1, t1, 1 / taur1, 1 / taud1)
        d2 = doubleExpFun(xSig, A2, A2, t2, 1 / taur2, 1 / taud2)

        # if np.any(np.array([A1, A2, t1, t2, itaur1, itaud1, itaur2, itaud2]) < 0)\
        #         or np.any(np.array([t1, t2]) < delayms - 10):
        #
        #     return np.ones_like(x) * 100
        # to avoid inverted double exponential for the lower delay one
        # elif (Ad1 < Ar1):
        #     return np.zeros_like(x)
        # else:
        return d1 - d2 + offset

olddir = "/home/maksutov/NIXFiles/exp_data/"
fdir = "/home/maksutov/NIXFiles/reorg/"

os.system("rm -rf "+fdir)
os.system("cp -r "+olddir+" "+fdir)

toAdd = "/home/maksutov/NIXFiles/bestPars.json"
j = json.load(open(toAdd))
x = np.array(j["xData"])
for i in j["bestPars"].keys():
    params = j["bestPars"][i]
    y = twoDoubleExps(x, *list(params))
    plt.plot(x, y, label = i)
    fname = fdir+i+".h5"
    print fname
    f = nix.File.open(str(fname), nix.FileMode.ReadWrite)
    try:

        if "FittingTraces" in f.blocks:
            blk = f.blocks["FittingTraces"]
        else: blk = f.create_block("FittingTraces", "FittingData")

        if not "FittingData" in blk.data_arrays:
            sampI = (x[-1]-x[0])/(len(x)-1)
            sig = neo.AnalogSignal(y, units="mV", sampling_rate=1000*Hz/sampI, t_start=x[0]*qs.ms, name="FittingData")
            nx.addAnalogSignal2Block(blk, sig)
        arr = blk.data_arrays["FittingData"]
        presec = f.sections["VibrationStimulii-Processed"
            ].sections["ContinuousStimulii"].sections["ContinuousStimulusAt265.0"]
        if "Fitting1" in presec:
            sec = presec["Fitting1"]
        else: sec = presec.create_section("Fitting1", "TwoExpFitting")
        pnames = ["A1", "A2", "t1", "t2", "taur1", "taud1", "taur2", "taud2", "offset"]
        punits = ["mV", "mV", "ms", "ms", "ms", "ms", "ms", "ms", "mV"]
        for ind in range(len(pnames)):
            if not pnames[ind] in sec.props:
                nx.addQuantity2section(sec, qs.Quantity(params[ind], punits[ind]), pnames[ind])
        if not "Tag1" in blk.tags:
            tag = nx.addTag("Tag1", "FittingData", position = float(x[0]), extent = float(x[-1]-x[0]), blk = blk, refs = [arr], metadata=sec)
    finally:
        f.close()
plt.legend()
plt.xlabel("time, ms")
plt.ylabel("voltage, mV")
plt.show()
'''