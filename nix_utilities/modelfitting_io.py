import nixio as nix
import os
import neoNIXIO as nio
import pickle

class modelfitting_io(object):
    '''
    Class provides functions to write fitting trials into nix files
    '''
    ModelFitting = "ModelFitting"
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
        self.location = location
        self.pickle = os.path.join(location, exp)
        self.exp = exp
        if not os.path.exists(self.pickle): os.makedirs(self.pickle)
        path = os.path.join(location, exp+".h5")
        toCreate = False
        if not os.path.exists(path):
            toCreate = True
        self.file = nix.File.open(path, nix.FileMode.ReadWrite)
        if toCreate:
            self.file.create_section(self.ModelFitting, "Main Section")
            self.file.create_section(self.fittingInputs, "About inputs")
            self.file.create_section(self.expectedOutputs, "About outputs")
            self.file.create_block(self.fittingInputs, "analogsignals")
            self.file.create_block(self.expectedOutputs, "signals,spiketrains,spiketimes")
            self.file.create_block(self.simulations, "signals,spiketrains,spiketimes")

    def add_input(self, sig):
        '''
        Adds experimental input current to nix file
        :param sig: neo.AnalogSignal
        :return:
        '''
        nio.addAnalogSignal2Block(self.file.blocks[self.fittingInputs], sig)
        sec = self.file.sections[self.fittingInputs].create_section(sig.name, "info")
        sec["description"] = nix.Value(sig.description)

    def add_exp_output(self, sig, spk, description = ""):
        '''
        Adds experimental output to nix file
        :param sig: neo.AnalogSignal
        :param spk: neo.SpikeTrain
        :return:
        '''
        sec = self.file.sections[self.expectedOutputs].create_section(sig.name, "info")
        sec["description"] = nix.Value(description)
        sig.name = "signal "+sig.name
        dsig = nio.addAnalogSignal2Block(self.file.blocks[self.expectedOutputs], sig)
        dsig.metadata = sec
        pos = nio.createPosDA("spiketimes "+spk.name, spk.times.simplified, self.file.blocks[self.expectedOutputs])
        nio.addMultiTag("spiketrain "+spk.name, "spiketrain", pos, self.file.blocks[self.expectedOutputs], [dsig])

    def add_fitting(self, name, results, initial_params, input_name, output_name):
        sec = self.file.sections[self.ModelFitting].create_section(name, "fitting trial")
        fp = sec.create_section(self.best_pos, "parameters after fitting")
        for v in results.best_pos:
            fp[v] = nix.Value(results.best_pos[v])
        fp = sec.create_section(self.inits_i, "parameters before fitting")
        for k in results.parameters.params:
            fp[k] = [nix.Value(v) for v in results.parameters.params[k]]
        fp = sec.create_section(self.inits, "other parameters")
        for k in initial_params:
            fp[k] = nix.Value(initial_params[k])
        pickle.dump(results, open(os.path.join(self.pickle, name+self.fpickle_suff)))
        sec["input"] = nix.Value(str(input_name))
        sec["output"] = nix.Value(str(output_name))
        sec["input"].definition = "Name of input signal used for fitting;" \
                                  " look to the section '{0}'".format(self.fittingInputs)
        sec["output"].definition = "Name of output signal used for fitting;" \
                                  " look to the section '{0}'".format(self.expectedOutputs)

    def close(self):
        self.file.close()

    def __del__(self):
        self.file.close()