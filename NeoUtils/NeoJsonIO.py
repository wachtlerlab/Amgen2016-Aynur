import json
from NeoUtils.Signals import QuantityFromString
import numpy as np
import neo
from NeoUtils.NeoPlot import PlotLists


def AnalogSignalToDict(sig):
    res = {}
    if not sig is None:
        res["signal"] = list(sig.magnitude)
        res["units"] = str(sig.units)
        res["t_start"] = str(sig.t_start)
        res["sampling_period"] = str(sig.sampling_period)
        print "sampling_period", sig.sampling_period, res["sampling_period"]
        res["name"] = sig.name
        res["description"] = sig.description
    return res

def DictToAnalogSignal(dic):
    if dic is None: return None
    signal = dic.get("signal")
    units = dic.get("units")
    t_start = dic.get("t_start")
    sampling_period = dic.get("sampling_period")
    name = dic.get("name")
    description = dic.get("description")
    if signal!=None: signal = np.array(signal)
    if units!=None:
        units = QuantityFromString(units)
        units = units.units
    if t_start!=None:
        t_start = QuantityFromString(t_start)
    if sampling_period!=None:
        sampling_period = QuantityFromString(sampling_period)
    return neo.AnalogSignal(signal, t_start=t_start, sampling_period=sampling_period, units=units,
                            name=name, description=description)

def SpikeTrainToDict(spk):
    res = {}
    if not spk is None:
        res["times"] = list(spk.times.magnitude)
        res["units"] = str(spk.units)
        res["t_stop"] = str(spk.t_stop)
        res["name"] = spk.name
        res["description"] = spk.description
    return res

def DictToSpikeTrain(dic):
    if dic is None: return None
    times = dic.get("times")
    units = dic.get("units")
    t_stop = dic.get("t_stop")
    name = dic.get("name")
    description = dic.get("description")
    if times is None or units is None or t_stop is None: return None
    times = np.array(times)
    units = QuantityFromString(units)
    units = units.units
    t_stop = QuantityFromString(t_stop)
    return neo.SpikeTrain(times*units, t_stop, units, name=name, description=description)

def SaveSignal(sig, filename):
    dic = AnalogSignalToDict(sig)
    json.dump(dic, open(filename, "w"))

def SaveSpikeTrain(spk, filename):
    json.dump(SpikeTrainToDict(spk), open(filename, "w"))

def SaveResults(fname, sigs, spks):
    print "sigs, spks:", sigs, spks
    res = {}
    res["signals"]=[AnalogSignalToDict(sig) for sig in sigs]
    res["spikes"]=[SpikeTrainToDict(spk) for spk in spks]
    json.dump(res, open(fname, "w"))

def LoadJson(fname):
    inp = json.load(open(fname))
    sigs = inp.get("signals")
    spks = inp.get("spikes")
    if not sigs is None:
        sigs = [DictToAnalogSignal(sig) for sig in sigs]
    else: sigs = []
    signal = inp.get("signal")
    if not signal is None:
        sigs.append(DictToAnalogSignal(inp))
    if not spks is None:
        spks = [DictToSpikeTrain(spk) for spk in spks]
    else: spks = []
    times = inp.get("times")
    if not times is None:
        spks.append(DictToSpikeTrain(inp))
    return [sigs, spks]

def PlotJsonAnalogSignals(fname):
    di = LoadJson(fname)
    PlotLists([zip(di[0], [None]*len(di[0]))])