import os
import pickle
from NixUtils import neoNIXIO as nio
import nixio as nix
import quantities as q

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
    def __init__(self, exp, nixLocation, mode = nix.FileMode.ReadWrite):
        '''
        :param exp: experiment name (neuron name)
        :param nixLocation: directory, where corresponding file stored. Will be created new file with
        suitable structure, if not exists and mode allows write access
        '''
        self.__nixLocation = str(os.path.expanduser(nixLocation))
        self.__pickle = str(os.path.join(self.__nixLocation, exp))
        self.exp = str(exp)
        self.nixFilePath = str(os.path.join(self.__nixLocation, exp + ".h5"))
        print "File ",exp, " is open in ", nixLocation
        self.__initNixFile()

    def __initNixFile(self):
        '''
        Initializes NIX File, adds sections if they are absent
        :return: None
        '''
        if not os.path.exists(self.__pickle): os.makedirs(self.__pickle)
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
        self.closeNixFile()

    def openNixFile(self, mode = nix.FileMode.ReadWrite):
        '''
        Opens NIX file
        :param mode: nix.FileMode
        :return: None
        '''
        self.nixFile = nix.File.open(self.nixFilePath, mode)

    def AddIn(self, sig, name = None, description = None, safe = True):
        '''
        Adds experimental input current to nix file
        :param sig: neo.AnalogSignal
        :param name: str
        :param description: str
        :return: None
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        if name is None: name = sig.name
        if description is None: description = sig.description
        if name in self.GetInNames():
            if safe: raise Exception("Input '{0}' already exists".format(name))
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
        :return: None
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

    def AddFit(self, name, model, results = None, initials={}, in_name="", out_name="", description="",
               safe = True, returninfo = True, best_pos = {}, input_var = None, duration = None):
        '''
        Adds info about fitting into NIX file
        :param name: str, name of fitting (should be uniq)
        :param model: str, id of model or BrianUtils.Model
        :param results: brian.modelfitting.ModelFittingResults, results of fitting
        :param initials: dict, initial values, used for fitting
        :param in_name: str, input name
        :param out_name: str, output name
        :param description: str, add description to fitting info
        :param safe: bool, throw error or not (see EoR)
        :param returninfo: does results object have additional info (see brian.modelfitting.modelfitting)
        :return: name of fitting
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        name = name.replace(" ", "_")
        if self.EoR(not in_name in self.GetInNames(), "Input '{0}' not found".format(in_name), safe): return False
        if self.EoR(not out_name in self.GetOutNames(), "Output '{0}' not found".format(out_name), safe): return False
        if self.EoR(name in self.GetFitNames(), "Fitting '{0}' already exists".format(name), safe): return False
        if results==None:
            class B(object):
                def __init__(self):
                    self.params = {}
            class A(object):
                def __init__(self):
                    self.best_pos = best_pos
                    self.parameters = B()
                    self.args = [{"input_var":input_var}]
            results = A()
            if description=="": description = "Not-A-Fitting"
        else: pickle.dump(results, open(os.path.join(self.__pickle, name + self.fpickle_suff), "w"))
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
        sec["pickle"] = nix.Value(str(name+self.fpickle_suff))
        sec.props["pickle"].definition = "Pickle filename for results of fitting"
        sec["model"] = nix.Value(str(model))
        sec.props["model"].definition = "model id"
        sec["input"] = nix.Value(str(in_name))
        sec["duration"] = nix.Value(duration)
        sec["output"] = nix.Value(str(out_name))
        sec["input_var"] = nix.Value(str(results.args[-1]["input_var"]))
        sec.props["input"].definition = "Name of input signal used for fitting;" \
                                  " look to the section '{0}'".format(self.fittingInputs)
        sec.props["output"].definition = "Name of output signal used for fitting;" \
                                  " look to the section '{0}'".format(self.expectedOutputs)
        sec.definition = description
        return name

    def GetFit(self, name):
        '''
        To given fitting returns information, stored in this NIX File
        :param name: string, name of fitting
        :return: {"input":str, "output":str, "pickle":str, "model":str, "inits":dict, "fitted":dict, "input_var":str}
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        g = [v for v in self.nixFile.sections[self.modelFittings].sections if v.name == name]
        if len(g)==0: return None
        g = g[0]
        di = {}
        di["input"] = str(g.props["input"].values[0].value) if "input" in g.props else None
        di["output"] = str(g.props["output"].values[0].value) if "output" in g.props else None
        di["pickle"] = str(g.props["pickle"].values[0].value) if "pickle" in g.props else None
        di["duration"] = float(g.props["duration"].values[0].value) if "duration" in g.props else None
        di["model"] = str(g.props["model"].values[0].value) if "model" in g.props else None
        di["Gamma"] = float(g.props["Gamma"].values[0].value) if "Gamma" in g.props else None
        di["inits"] = {k.name:k.values[0].value for k in g.sections[self.inits]} if self.inits in g.sections else None
        # di["inits"].update({k:g.section[self.inits_i][k] for k in g.section[self.inits_i].props})
        di["fitted"] = {k.name: k.values[0].value for k in g.sections[self.best_pos].props}
        di["input_var"] = str(g.props["input_var"].values[0].value) if "input_var" in g.props else None
        return di

    def RmFit(self, name, safe = True):
        '''
        Removes fitting by givrn name. DOESN'T WORK, DON'T USE!!!
        :param name: str, name of fitting
        :param safe: bool
        :return: None
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        if self.EoR(not name in self.GetFitNames(), "Fitting '{0}' not found".format(name), safe): return False
        path = os.path.join(self.__pickle, name + self.fpickle_suff)
        if os.path.exists(path): os.remove(path)
        del self.nixFile.sections[self.modelFittings].sections[name]
        if name in self.GetSimNames():
            sec = [v for v in self.nixFile.sections[self.simulations] if v.name==name][0]
            blk = self.nixFile.blocks[self.simulations]
            for i in sec:
                tag = [t for t in blk.tags if t.metadata==i]
                for j in tag:
                    ar = [a for a in blk.data_arrays if j.references[0]==a]
                    for k in ar:
                        del k
                    del j
            for i in sec:
                del i

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

    def AddSim(self, fname, res, safe = True):
        '''
        Adds info about simulation to a fitting
        :param fname: fitting name
        :param res: results of simulation
        :param safe: if safe, will throw Exceptions, else only return False
        :return: None
        '''
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
        '''
        Returns simulation info
        :param fname: name of fitting (same to simulation name)
        :param safe: if safe, will throw Exceptions, else only return False
        :return: {"monitors":list of neo.AnalogSignal, "input":str, "output":str, "name":str}
        '''
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
        '''
        Returns input's names available in NIX File
        :return: list of str
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.fittingInputs].sections])

    def GetOutNames(self):
        '''
        Returns output's names available in NIX File
        :return: list of str
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.expectedOutputs].sections])

    def GetFitNames(self):
        '''
        Returns fitting's names available in NIX File
        :return: list of str
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.modelFittings].sections])

    def GetSimNames(self):
        '''
        Returns simulation's names available in NIX File
        :return: list of str
        '''
        if not self.nixFile.is_open(): self.openNixFile()
        return sorted([n.name for n in self.nixFile.sections[self.simulations].sections])

    def flt(self, q):
        '''
        gives float representation of given quantity
        :param q: quantities.Quantity
        :return: float
        '''
        return float(q.simplified.magnitude)

    def EoR(self, condition, text, safe = True):
        '''
        Internal function, for shorter code. If condition is True, throws Exception or returns True, depending on safe
        :param condition: bool
        :param text: str, Exception message
        :param safe: bool
        :return:
        '''
        if condition:
            if safe: raise Exception(text+"\n"+str(self.nixFilePath))
            else: return True
        else: return False

    def GetUniqName(self, pref, arr):
        '''
        Returns uniq name for given array of existing names and prefix, adds only number at the end
        :param pref: str
        :param arr: list of str
        :return: str
        '''
        for i in xrange(123456):
            name = pref+str(i)
            if not name in arr:
                return name
        raise Exception("No suitable option")

    def closeNixFile(self):
        '''
        Closes NIX file
        :return:
        '''
        if self.nixFile.is_open():
	    self.nixFile.close()

    def __del__(self):
        self.closeNixFile()
