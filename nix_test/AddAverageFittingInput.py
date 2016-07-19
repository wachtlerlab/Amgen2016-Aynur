from matplotlib import pylab as plt
import numpy as np
import neo
import json
import nixio as nix
import neoNIXIO as nx
from quantities import Hz
import quantities as qs
import rawDataProcess as rd

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

fdir = "/home/maksutov/NIXFiles/reorg/"
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

        if "FittingCurves" in f.blocks:
            blk = f.blocks["FittingCurves"]
        else: blk = f.create_block("FittingCurves", "FittingData")

        if not "FittingData" in blk.data_arrays:
            sampI = (y[-1]-y[0])/(len(y)-1)
            sig = neo.AnalogSignal(y, "mV", sampling_rate=1000*Hz/sampI, name="FittingData")
            nx.addAnalogSignal2Block(blk, sig)

        presec = f.sections["VibrationStimulii-Processed"
            ].sections["ContinuousStimulii"].sections["ContinuousStimulusAt265.0"]
        if "twoExpFitting" in presec:
            sec = presec["twoExpFitting"]
        else: sec = presec.create_section("twoExpFitting", "FittingModelData")
        pnames = ["A1", "A2", "t1", "t2", "taur1", "taud1", "taur2", "taud2", "offset"]
        punits = ["mV", "mV", "ms", "ms", "ms", "ms", "ms", "ms", "mV"]
        for ind in range(len(pnames)):
            if not pnames[ind] in sec.props:
                nx.addQuantity2section(sec, qs.Quantity(params[ind], punits[ind]), pnames[ind])
        if not "TwoExpCurve" in blk.tags:
            tag = rd.addTag("TwoExpCurve", "FittingDataTag", position = [x[0], x[-1]], blk = blk, refs = [], metadata=sec)
    finally:
        f.close()
plt.legend()
plt.xlabel("time, ms")
plt.ylabel("voltage, mV")
plt.show()
