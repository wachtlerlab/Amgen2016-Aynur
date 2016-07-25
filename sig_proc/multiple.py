import nix_utilities.rawDataAnalyse as rd
from nix_utilities.neoNIXIO import tag2AnalogSignal
import quantities as q, numpy as np
import plot as pl
import signals as ss
import sig_proc.signal_converter as sconv

import neo

labels = ["Trial", "PredictedInput"]
YesDict = labels[:1]

def ReadExperiment(ename):
    dirname = "/home/maksutov/NIXFiles/reorg/"
    freqs = [265]
    try:
        analyser=rd.RawDataAnalyser(ename, dirname)
    except:
        print "analyser=rd.RawDataAnalyser(i, dirname)"
    data = [t for t in analyser.getContResps(freqs)[freqs[0]] if len(t)>0]
    block = neo.Block(name = ename, description="experimental data")
    spk = analyser.getContSpikes(freqs=freqs, types=None)[freqs[0]]
    Ds, Bs, As = "DuringStimulus", "BeforeStimulus", "AfterStimulus"
    seg = neo.Segment("DuringStimulus", "ExpData")
    for i in xrange(len(data)):
        sc = data[i]
        sp = spk[i]
        if not(Ds in sc and As in sc and Bs in sc): continue
        median = np.median(np.concatenate((sc[Bs].magnitude/sc[Bs].units, sc[As].magnitude/sc[As].units)))*sc[Ds].units
        interm = sc[Ds] - ss.SignalBuilder(sc[Ds]).get_constant(median)
        signal = sconv.BeginSignalOn(interm, 0*q.s)
        signal = signal[signal.times < 1*q.s]
        signal.name = "Trial"+str(i+1)
        signal.description = "voltage"
        sh_spk = sconv.ShiftSpikeTrain(sp[Ds], interm.times[0])
        sh_spk.name = signal.name
        sh_spk.description = "spikes"
        seg.analogsignals.append(signal)
        seg.spiketrains.append(sh_spk)

    myExpSect = analyser.nixFile.sections["VibrationStimulii-Processed"].sections["ContinuousStimulii"
    ].sections["ContinuousStimulusAt265.0"].sections
    for j in myExpSect:
        if "Fitting"!=j.name[:7]: continue
        myFitTag = [t for t in analyser.nixFile.blocks["FittingTraces"].tags if t.metadata == myExpSect[j.name]]
        res = tag2AnalogSignal(myFitTag[0], 0)
        res.name = labels[1]+j.name[7:]
        res.description = "Current"
        seg.analogsignals.append(res)

    block.segments.append(seg)
    return block


def YesName(stri):
    for i in YesDict:
        if i in stri:
            return True
    return False

def PlotExperiment(block, subplots=True, func = YesName):
    pl.plot_block(block, subplots, func)
