from NixUtils import ModelfittingIO as mio
from Storage import ProjectStructure as ps
from NixUtils import rawDataAnalyse as rd
from NeoUtils import Signals as ss
import  quantities as q
import sys, os, json
import numpy as np

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
        return d1 - d2 + offset


originalsFolder = sys.argv[1]
ps.createFolders()

NameBestPars = os.path.join(originalsFolder, "bestPars.json")
bestPars = json.load(open(NameBestPars))

x = np.array(bestPars["xData"])

params = bestPars["bestPars"]
for ename in params:
    fileName = os.path.join(originalsFolder, ename + ".h5")
    y = twoDoubleExps(x, *list(params[ename]))
    xQ = x*q.ms
    sampling_period = (xQ[-1]-xQ[1])/(len(xQ)-1)
    subthreshold = ss.neo.AnalogSignal(y, units=q.mV, sampling_period=sampling_period, t_start=xQ[0])
    subthreshold.name = "subthreshold"
    subthreshold.description = "voltage"
    analyser = rd.RawDataAnalyser(ename, originalsFolder)
    signals = [t for t in analyser.getContResps([265])[265] if len(t) > 0]
    spikes = analyser.getContSpikes(freqs=[265], types=None)[265]
    del analyser, x, xQ, y
    f = mio.ModelfittingIO(ename, ps.FITTING)
    f.AddIn(subthreshold)
    timemaxDA = 0 * q.s
    for i in xrange(len(signals)):
        for subS in ["BeforeStimulus", "DuringStimulus", "AfterStimulus"]:
            if subS in signals[i]:
                sig = signals[i][subS]
                spk = spikes[i][subS]
                sig.name = "Trial"+str(i)+"-"+subS
                sig.description = "voltage"
                spk.name = signals[i][subS].name
                spk.description = "spiketrain"
                f.AddOut(sig, spk)
        if "DuringStimulus" in signals[i] and "AfterStimulus" in signals[i]:
            name = "Trial"+str(i)+"-"+"DuringAfterStimulus"
            sigD = signals[i]["DuringStimulus"]
            spkD = spikes[i]["DuringStimulus"]
            sigA = signals[i]["AfterStimulus"]
            spkA = spikes[i]["AfterStimulus"]
            sig = ss.Concat(sigD, sigA, name=name, description="voltage")
            spk = ss.JoinSpikeTrains([spkD, spkA])
            if sig.times[-1]>timemaxDA: timemaxDA = sig.times[-1]
            f.AddOut(sig, spk)
    subthresholdDA = ss.ExpandNull(subthreshold, timemaxDA)
    subthresholdDA.name = subthreshold.name+"-DuringAfterStimulus"
    f.AddIn(subthresholdDA)
    f.AddIn(subthresholdDA*1e-7, name=subthresholdDA.name+"-e-7")
    dermag = np.gradient(subthreshold.magnitude)/(subthreshold.sampling_period.simplified.magnitude)
    derivative = ss.neo.AnalogSignal(dermag, sampling_period=subthreshold.sampling_period, t_start=subthreshold.t_start,
                                     units = q.nA)
    f.AddIn(derivative, name = "derivative", description = "current")
    derivativeDA = ss.ExpandNull(derivative, timemaxDA)
    f.AddIn(derivativeDA, name = "derivative-DuringAfterStimulus", description = "current")