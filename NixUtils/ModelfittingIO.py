import os
import json
import pickle
import numpy as np
import quantities as q

import neo
import nixio as nix
import neoNIXIO as nio

from NixUtils import rawDataAnalyse as rd, ProjectFileStructure as fs
from NeoUtils import Signals as ss

class ModelfittingIO(object):
    '''
    Class provides functions to write fitting trials into nix files
    '''
    modelFittings = "modelFittings"
    fittingInputs = "fittingInputs"
    expectedOutputs = "expectedOutputs"
    simulations = "simulations"
    best_pos = "best_pos"
    inits_i = "initial_intervals"
    inits = "initials"
    fpickle_suff = ".fitting.pickle"
    def __init__(self, exp, nixLocation):
        '''
        :param exp:
        :param nixLocation:
        '''
        self.__nixLocation = str(os.path.expanduser(nixLocation))
        self.__pickle = str(os.path.join(self.__nixLocation, exp))
        self.exp = str(exp)
        self.nixFilePath = str(os.path.join(self.__nixLocation, exp + ".h5"))
        self.__initNixFile()
        print "Experiment {0} from {1} is open".format(exp, nixLocation)

    def __initNixFile(self):
        if not os.path.exists(self.__pickle): os.makedirs(self.__pickle)
        if os.path.exists(self.nixFilePath):
            self.nixFile = nix.File.open(self.nixFilePath, nix.FileMode.ReadWrite)
            blks = [(self.fittingInputs, "analogsignals"),
                    (self.expectedOutputs, "signals,spiketrains,spiketimes"),
                    (self.simulations, "signals,spiketrains,spiketimes")]
            scs = [(self.modelFittings, "All fittings' list"),
                   (self.fittingInputs, "About inputs"),
                   (self.expectedOutputs, "About outputs"),
                   (self.simulations, "Simulations' list")]
            for b in blks:
                if not b[0] in [i.name for i in self.nixFile.blocks]:
                    self.nixFile.create_block(b[0], b[1])
            for s in scs:
                if not s[0] in self.nixFile.sections:
                    self.nixFile.create_section(s[0], s[1])
        else: self.nixFile = nix.File.open(self.nixFilePath, nix.FileMode.ReadWrite)

    def openNixFile(self, mode = nix.FileMode.ReadWrite):
        self.nixFile = nix.File.open(self.nixFilePath, mode)

    def AddIn(self, sig, name = None, description = None, safe = True):
        '''
        Adds experimental input current to nix file
        :param sig: neo.AnalogSignal
        :param name: str
        :param description: str
        :return:
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        if name is None: name = sig.name
        if description is None: description = sig.description
        if name in self.GetInNames():
            if safe: raise Exception("Input '{0}' already exists")
        blk = self.nixFile.blocks[self.fittingInputs]
        sig.name = name
        asig = nio.addAnalogSignal2Block(blk, sig)
        sec = self.nixFile.sections[self.fittingInputs].create_section(name, "info")
        sec.definition = description
        nio.addQuantity2section(sec, sig.sampling_period, "sampling_period")
        nio.addQuantity2section(sec, sig.t_start, "t_start")
        nio.addQuantity2section(sec, sig.duration, "duration")
        nio.addQuantity2section(sec, sig.units, "units")
        nio.addTag("whole "+name, "whole signal tag", self.flt(sig.t_start),
                         blk, [asig], sec, self.flt(sig.duration))

    def AddOut(self, sig, spk, name = None, description = None, safe = True):
        '''
        Adds experimental output to nix file
        :param sig: neo.AnalogSignal
        :param spk: neo.SpikeTrain
        :return:
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        if name is None: name = sig.name
        if description is None: description = sig.description
        if self.EoR(name in self.GetOutNames(), "Output '{0}' already exists".format(name), safe): return False
        sec = self.nixFile.sections[self.expectedOutputs].create_section(name, "info")
        sec.definition = description
        blk = self.nixFile.blocks[self.expectedOutputs]
        sig.name = name
        dsig = nio.addAnalogSignal2Block(blk, sig)
        pos = nio.createPosDA("spiketimes "+name, spk.times.simplified, blk)
        nio.addMultiTag("spiketrain "+name, "spiketrain multitag", pos, blk, [dsig], sec)
        nio.addTag("whole " + name, "whole signal tag", self.flt(sig.t_start),
                   blk, [dsig], sec, self.flt(sig.duration))

    def AddFit(self, name, model, results = None, initials={}, in_name="", out_name="", description ="", safe = True):
        if not self.nixFile.is_open(): self.openNixFile()
        name = name.replace(" ", "_")
        if self.EoR(not in_name in self.GetInNames(), "Input '{0}' not found".format(in_name), safe): return False
        if self.EoR(not out_name in self.GetOutNames(), "Output '{0}' not found".format(out_name), safe): return False
        if self.EoR(name in self.GetFitNames(), "Fitting '{0}' already exists".format(name), safe): return False
        if results==None:
            results = object()
            results.best_pos = {}
            results.parameters = object()
            results.parameters.params = {}
            if description=="": description = "Not-A-Fitting"
        sec = self.nixFile.sections[self.modelFittings].create_section(name, "fitting trial")
        fp = sec.create_section(self.best_pos, "parameters after fitting")
        for v in results.best_pos:
            fp[v] = nix.Value(results.best_pos[v])
        fp = sec.create_section(self.inits_i, "parameters before fitting")
        for k in results.parameters.params:
            fp[k] = [nix.Value(v) for v in results.parameters.params[k]]
        fp = sec.create_section(self.inits, "other parameters")
        for k in initials:
            fp[k] = nix.Value(initials[k])
        pickle.dump(results, open(os.path.join(self.__pickle, name + self.fpickle_suff), "w"))
        sec["pickle"] = nix.Value(str(name+self.fpickle_suff))
        sec.props["pickle"].definition = "Pickle filename for results of fitting"
        sec["model"] = nix.Value(str(model))
        sec.props["model"].definition = "model id"
        sec["input"] = nix.Value(str(in_name))
        sec["output"] = nix.Value(str(out_name))
        sec["input_var"] = nix.Value(str(results.args[-1]["input_var"]))
        sec.props["input"].definition = "Name of input signal used for fitting;" \
                                  " look to the section '{0}'".format(self.fittingInputs)
        sec.props["output"].definition = "Name of output signal used for fitting;" \
                                  " look to the section '{0}'".format(self.expectedOutputs)
        sec.definition = description
        return name

    def RmFit(self, name, safe = True):
        if not self.nixFile.is_open(): self.openNixFile()
        if self.EoR(not name in self.GetFitNames(), "Fitting '{0}' not found".format(name), safe): return False
        path = os.path.join(self.__pickle, name + self.fpickle_suff)
        if os.path.exists(path): os.remove(path)
        del self.nixFile.sections[self.modelFittings].sections[name]

    def GetIn(self, name):
        '''
        Returns input signal for given name from nix file
        :param name: name of input signal
        :return: neo.AnalogSignal
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        g = [v for v in self.nixFile.sections[self.fittingInputs].sections if v.name == name]
        if len(g)==0: return None
        g = g[0]
        sgs = [m for m in self.nixFile.blocks[self.fittingInputs].tags if m.metadata == g]
        if len(sgs)==0: return None
        sig = nio.tag2AnalogSignal(sgs[0], 0)
        sig.name = name
        return sig

    def GetOut(self, name):
        '''
        Returns expected output signal and spiketrain for given name from nix file
        :param name: name of output
        :return: neo.Analogsignal, neo.SpikeTrain
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        g = [v for v in self.nixFile.sections[self.expectedOutputs].sections if v.name == name]
        if len(g)==0: return None, None
        g = g[0]
        sgs = [m for m in self.nixFile.blocks[self.expectedOutputs].tags if m.metadata == g]
        spks = [m for m in self.nixFile.blocks[self.expectedOutputs].multi_tags if m.metadata == g]
        if len(sgs)==0: return None, None
        sig = nio.tag2AnalogSignal(sgs[0], 0)
        sig.name = name
        spk = nio.multiTag2SpikeTrain(spks[0], sig.t_start, sig.t_start+sig.duration) if len(spks)>0 else None
        return sig, spk

    def GetFit(self, name):
        if not self.nixFile.is_open(): self.openNixFile()
        g = [v for v in self.nixFile.sections[self.modelFittings].sections if v.name == name]
        if len(g)==0: return None
        g = g[0]
        di = {}
        di["input"] = str(g.props["input"].values[0].value)
        di["output"] = str(g.props["output"].values[0].value)
        di["pickle"] = str(g.props["pickle"].values[0].value)
        di["model"] = str(g.props["model"].values[0].value)
        di["inits"] = {k.name:k.values[0].value for k in g.sections[self.inits].props}
        # di["inits"].update({k:g.section[self.inits_i][k] for k in g.section[self.inits_i].props})
        di["fitted"] = {k.name: k.values[0].value for k in g.sections[self.best_pos].props}
        di["input_var"] = str(g.props["input_var"].values[0].value)
        return di

    def AddSim(self, fname, res, safe = True):
        if not self.nixFile.is_open(): self.openNixFile()
        if self.EoR(not fname in self.GetFitNames(), "Fitting '{0}' not found".format(fname), safe): return False
        if self.EoR(fname in self.GetSimNames(), "Simulation '{0}' already exists".format(fname), safe): return False
        sec = self.nixFile.sections[self.simulations].create_section(fname, "simulation metadata")
        sec.definition = self.GetUniqName("simulation", [n.definition for n in self.nixFile.sections[self.simulations]])
        blk = self.nixFile.blocks[self.simulations]
        mons = sec.create_section("monitors", "simulation tracks")
        for i in res:
            ns = mons.create_section(i.name, "monitor")
            ns.definition = i.description
            name = i.name
            i.name = fname + " " + name
            da = nio.addAnalogSignal2Block(blk, i)
            tagname = fname + " whole " + name
            nio.addTag(tagname, "analogsignal", self.flt(i.t_start), blk, [da], ns, self.flt(i.duration))

    def GetSim(self, fname, safe = True):
        if not self.nixFile.is_open(): self.openNixFile()
        v = [s for s in self.nixFile.sections[self.simulations].sections if s.name == fname]
        if self.EoR(len(v)==0, "Simulation {0} doesn't exist".format(fname), safe): return False
        v = v[0]
        f = self.GetFit(fname)
        res = {}
        sigs = []
        for i in v.sections["monitors"].sections:
            arr = [a for a in self.nixFile.blocks[self.simulations].tags if a.metadata == i]
            if len(arr)>0:
                ns = nio.tag2AnalogSignal(arr[0], 0)
                ns.name = i.name
                ns.description = i.definition
                sigs.append(ns)
        res["name"] = fname
        res["input"] = f["input"]
        res["output"] = f["output"]
        res["monitors"] = sigs
        return res

    def GetInNames(self):
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.fittingInputs].sections])

    def GetOutNames(self):
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.expectedOutputs].sections])

    def GetFitNames(self):
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.modelFittings].sections])

    def GetSimNames(self):
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.simulations].sections])

    def flt(self, q):
        return float(q.simplified.magnitude)

    def EoR(self, condition, text, safe = True):
        if condition:
            if safe: raise Exception(text)
            else: return True
        else: return False

    def GetUniqName(self, pref, arr):
        for i in xrange(123456):
            name = pref+str(i)
            if not name in arr:
                return name
        raise Exception("No suitable option")

    def closeNixFile(self):
        self.nixFile.close()

    def __del__(self):
        self.nixFile.close()

def ReadExperiment(ename, default = ["Trial", "PredictedInput"], labels = None):
    labels = default if labels==None else None
    freqs = [265]
    analyser=rd.RawDataAnalyser(ename, fs.reorg)
    data = [t for t in analyser.getContResps(freqs)[freqs[0]] if len(t)>0]
    block = neo.Block(name = ename, description="experimental data")
    spk = analyser.getContSpikes(freqs=freqs, types=None)[freqs[0]]
    Ds, Bs, As = "DuringStimulus", "BeforeStimulus", "AfterStimulus"
    seg = neo.Segment("DuringStimulus", "ExpData")
    seg_af = neo.Segment("AfterStimulus", "ExpData")
    for i in xrange(len(data)):
        sc = data[i]
        sp = spk[i]
        if not(Ds in sc and As in sc and Bs in sc): continue
        median = np.median(np.concatenate((sc[Bs].magnitude/sc[Bs].units, sc[As].magnitude/sc[As].units)))*sc[Ds].units

        interm = sc[Ds] - ss.SignalBuilder(sc[Ds]).get_constant(median)
        signal = ss.BeginSignalOn(interm, 0 * q.s)
        signal.name = "Trial"+str(i+1)
        signal.description = "voltage"
        sh_spk = ss.ShiftSpikeTrain(sp[Ds], - interm.times[0])
        sh_spk.name = signal.name
        sh_spk.description = "spikes"
        seg.analogsignals.append(signal)
        seg.spiketrains.append(sh_spk)

        interm = sc[As] - ss.SignalBuilder(sc[As]).get_constant(median)
        signal = ss.BeginSignalOn(interm, 0 * q.s)
        length = 0.5*q.s
        signal = signal[signal.times < length]
        signal.name = "Trial"+str(i+1)
        signal.description = "voltage"
        sh_spk = ss.ShiftSpikeTrain(sp[As], - interm.times[0])
        sh_spk = sh_spk[sh_spk < length]
        sh_spk.name = signal.name
        sh_spk.description = "spikes"
        seg_af.analogsignals.append(signal)
        seg_af.spiketrains.append(sh_spk)
        
    if default[1] in labels:
        myExpSect = analyser.nixFile.sections["VibrationStimulii-Processed"].sections["ContinuousStimulii"
        ].sections["ContinuousStimulusAt265.0"].sections
        for j in myExpSect:
            if "Fitting"!=j.name[:7]: continue
            myFitTag = [t for t in analyser.nixFile.blocks["FittingTraces"].tags if t.metadata == myExpSect[j.name]]
            print "myFitTag", myFitTag
            res = nio.tag2AnalogSignal(myFitTag[0], 0)
            res = res[res.times<1*q.s]
            res.name = labels[1]+j.name[7:]
            res.description = "voltage"
            seg.analogsignals.append(res)
            tcur = neo.AnalogSignal(res.magnitude, units=q.nA, t_start=res.t_start, sampling_period=res.sampling_period)
            tcur.name=res.name+"-1"
            tcur.description="current"
            seg.analogsignals.append(tcur)
            mag = res.sampling_rate.simplified.magnitude*np.gradient(res.magnitude)
            res = neo.AnalogSignal(mag, t_start=res.t_start, sampling_period=res.sampling_period, units=q.nA)
            res.name = labels[1]+j.name[7:]
            res.description = "current"
            seg.analogsignals.append(res)

    block.segments.append(seg)
    block.segments.append(seg_af)

    return block

def PickleExp(ename, default = ["Trial", "PredictedInput"], labels = None):
    blk = ReadExperiment(ename, default, labels)
    if not os.path.exists(fs.nxpickle):
        os.makedirs(fs.nxpickle)
    pickle.dump(blk, open(os.path.join(fs.nxpickle, ename+".pickle"), "w"))

def UnpickleExp(ename):
    path = os.path.join(fs.nxpickle, ename+".pickle")
    blk = pickle.load(open(path)) if os.path.exists(path) else None
    return blk

def GetAvaliableIds():
    path = os.path.join(fs.DATA, "ids_with_input")
    if os.path.exists(path):
        di = json.load(open(path))
        return di["ids"]
    else: return []

if __name__=="__main__":
    for k in GetAvaliableIds():
        PickleExp(str(k))
