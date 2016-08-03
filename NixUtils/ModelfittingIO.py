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
    def __init__(self, exp, location):
        '''
        :param exp:
        :param location:
        '''
        self.__location = str(location)
        self.__pickle = str(os.path.join(location, exp))
        self.exp = str(exp)
        self.path = str(os.path.join(location, exp+".h5"))
        self.open()

    def open(self):
        if not os.path.exists(self.__pickle): os.makedirs(self.__pickle)
        toCreate = False
        if not os.path.exists(self.path):
            toCreate = True
        self.file = nix.File.open(self.path, nix.FileMode.ReadWrite)
        if toCreate:
            self.file.create_section(self.modelFittings, "Main Section")
            self.file.create_section(self.fittingInputs, "About inputs")
            self.file.create_section(self.expectedOutputs, "About outputs")
            self.file.create_block(self.fittingInputs, "analogsignals")
            self.file.create_block(self.expectedOutputs, "signals,spiketrains,spiketimes")
            self.file.create_block(self.simulations, "signals,spiketrains,spiketimes")


    def add_input(self, sig, name = None, description = None, safe = False):
        '''
        Adds experimental input current to nix file
        :param sig: neo.AnalogSignal
        :param name: str
        :param description: str
        :return:
        '''
        if name is None: name = sig.name
        if description is None: description = sig.description
        if name in self.get_input_names():
            if safe: raise Exception("Input '{0}' already exists")
        blk = self.file.blocks[self.fittingInputs]
        sig.name = name
        asig = nio.addAnalogSignal2Block(blk, sig)
        sec = self.file.sections[self.fittingInputs].create_section(name, "info")
        sec.definition = description
        nio.addQuantity2section(sec, sig.sampling_period, "sampling_period")
        nio.addQuantity2section(sec, sig.t_start, "t_start")
        nio.addQuantity2section(sec, sig.duration, "duration")
        nio.addQuantity2section(sec, sig.units, "units")
        nio.addTag("whole "+name, "whole signal tag", float(sig.t_start.simplified.magnitude),
                         blk, [asig], sec, float(sig.duration.simplified.magnitude))

    def add_exp_output(self, sig, spk, name = None, description = None, safe = False):
        '''
        Adds experimental output to nix file
        :param sig: neo.AnalogSignal
        :param spk: neo.SpikeTrain
        :return:
        '''
        if name is None: name = sig.name
        if description is None: description = sig.description
        if name in self.get_output_names():
            if safe: raise Exception("Output '{0}' already exists".format(name))
            else: return False
        sec = self.file.sections[self.expectedOutputs].create_section(name, "info")
        sec.definition = description
        blk = self.file.blocks[self.expectedOutputs]
        dsig = nio.addAnalogSignal2Block(blk, sig)
        pos = nio.createPosDA("spiketimes "+name, spk.times.simplified, blk)
        nio.addMultiTag("spiketrain "+name, "spiketrain multitag", pos, blk, [dsig], sec)
        nio.addTag("whole "+name, "whole signal tag", float(sig.t_start.simplified.magnitude),
                   blk, [dsig], sec, float(sig.duration.simplified.magnitude))

    def add_fitting(self, name, results, initials={}, input_name="", output_name="", description ="", safe = False):
        b1=b2=b3=False
        if not input_name in self.get_input_names(): b1 = True
        if not output_name in self.get_output_names(): b2 = True
        if name in self.get_fitting_names(): b3 = True
        if safe:
            if b1: raise Exception("Input '{0}' not found".format(output_name))
            if b2: raise Exception("Input '{0}' not found".format(input_name))
            if b3: raise Exception("Fitting '{0}' already exists".format(name))
        elif b1 or b2 or b3: return False
        sec = self.file.sections[self.modelFittings].create_section(name, "fitting trial")
        fp = sec.create_section(self.best_pos, "parameters after fitting")
        for v in results.best_pos:
            fp[v] = nix.Value(results.best_pos[v])
        fp = sec.create_section(self.inits_i, "parameters before fitting")
        for k in results.parameters.params:
            fp[k] = [nix.Value(v) for v in results.parameters.params[k]]
        fp = sec.create_section(self.inits, "other parameters")
        for k in initials:
            fp[k] = nix.Value(initials[k])
        pickle.dump(results, open(os.path.join(self.__pickle, name + self.fpickle_suff)))
        sec["pickle"] = nix.Value(str(name+self.fpickle_suff))
        sec["pickle"].definition = "Pickle filename for results of fitting"
        sec["input"] = nix.Value(str(input_name))
        sec["output"] = nix.Value(str(output_name))
        sec["input"].definition = "Name of input signal used for fitting;" \
                                  " look to the section '{0}'".format(self.fittingInputs)
        sec["output"].definition = "Name of output signal used for fitting;" \
                                  " look to the section '{0}'".format(self.expectedOutputs)
        sec.definition = description

    def get_input(self, name):
        '''
        Returns input signal for given name from nix file
        :param name: name of input signal
        :return: neo.AnalogSignal
        '''
        g = [v for v in self.file.sections[self.fittingInputs].sections if v.name==name]
        if len(g)==0: return None
        g = g[0]
        sgs = [m for m in self.file.blocks[self.fittingInputs].tags if m.metadata==g]
        if len(sgs)==0: return None
        sig = nio.tag2AnalogSignal(sgs[0], 0)
        sig.name = name
        return sig

    def get_output(self, name):
        '''
        Returns expected output signal and spiketrain for given name from nix file
        :param name: name of output
        :return: neo.Analogsignal, neo.SpikeTrain
        '''
        g = [v for v in self.file.sections[self.expectedOutputs].sections if v.name==name]
        if len(g)==0: return None, None
        g = g[0]
        sgs = [m for m in self.file.blocks[self.expectedOutputs].tags if m.metadata==g]
        spks = [m for m in self.file.blocks[self.expectedOutputs].multi_tags if m.metadata==g]
        if len(sgs)==0: return None, None
        sig = nio.tag2AnalogSignal(sgs[0], 0)
        sig.name = name
        spk = nio.multiTag2SpikeTrain(spks[0], sig.t_start, sig.t_start+sig.duration) if len(spks)>0 else None
        return sig, spk

    def get_fitting(self, name):
        g = [v for v in self.file.sections[self.modelFittings].sections if v.name==name]
        if len(g)==0: return None
        g = g[0]


    def get_input_names(self):
        return [n.name for n in self.file.sections[self.fittingInputs].sections]

    def get_output_names(self):
        return [n.name for n in self.file.sections[self.expectedOutputs].sections]

    def get_fitting_names(self):
        return [n.name for n in self.file.sections[self.modelFittings].sections]

    def close(self):
        self.file.close()

    def __del__(self):
        self.file.close()

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
        # signal = signal[signal.times < 1*q.s]
        signal.name = "Trial"+str(i+1)
        signal.description = "voltage"
        sh_spk = ss.ShiftSpikeTrain(sp[Ds], -interm.times[0])
        sh_spk.name = signal.name
        sh_spk.description = "spikes"
        seg.analogsignals.append(signal)
        seg.spiketrains.append(sh_spk)

        interm = sc[As] - ss.SignalBuilder(sc[As]).get_constant(median)
        signal = ss.BeginSignalOn(interm, 0 * q.s)
        signal = signal[signal.times < 0.1*q.s]
        signal.name = "Trial"+str(i+1)
        signal.description = "voltage"
        sh_spk = ss.ShiftSpikeTrain(sp[As], - interm.times[0])
        sh_spk.name = signal.name
        sh_spk.description = "spikes"
        seg.analogsignals.append(signal)
        seg_af.spiketrains.append(sh_spk)
        
    if default[1] in labels:
        myExpSect = analyser.nixFile.sections["VibrationStimulii-Processed"].sections["ContinuousStimulii"
        ].sections["ContinuousStimulusAt265.0"].sections
        for j in myExpSect:
            if "Fitting"!=j.name[:7]: continue
            myFitTag = [t for t in analyser.nixFile.blocks["FittingTraces"].tags if t.metadata == myExpSect[j.name]]
            print "myFirTag", myFitTag
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
