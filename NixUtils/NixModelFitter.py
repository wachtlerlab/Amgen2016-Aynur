from BrianUtils import ModelFitter as MF
from BrianUtils import NeuronModels as NM
from BrianUtils import Simulator as S
from BrianUtils.Utilities import TimeToBrian
from NixUtils import ModelfittingIO as MIO
from NixUtils import ProjectFileStructure as FS
from NeoUtils import NeoPlot as PL
from NeoUtils import NeoJsonIO as nio
import datetime as dt
import os

class NixModelFitter(object):
    '''
    Class provides high-level functions for modelfitting, simulations and plotting with certain NIX Files structure
    and directories structure,
    provided by ProjectFileStructure.py
    '''
    def __init__(self, expname, dir = None, mode = "w"):
        '''
        Creates new instance of NixModelFitter object
        :param expname: str, name of experimtent
        :param dir: str, directory, where corresponding NIX File with inputs and outputs is stored or will be created
                                (see NixUtils.ModelfittingIO.ModelfittingIO)
        :param mode: str from {"w":ReadWrite, "r":ReadOnly}.keys()
        '''
        if dir is None: dir = FS.FITTING
        if mode == "w":
            self.file = MIO.ModelfittingIO(expname, dir, mode = MIO.nix.FileMode.ReadWrite)
        else:
            self.file = MIO.ModelfittingIO(expname, dir, mode = MIO.nix.FileMode.ReadOnly)

    def FitModel(self, model, input, output, inits = {}, popsize=1000, maxiter=100, algoptparams = {}, algo ="CMAES",
                 from_perc = True, optparams = None, returninfo = True, logstr = None):
        '''
        Fits model to output recording using given input and model within own NIX File. Writes parameters and fitting
        info into NIX File.
        :param model: str, id of model will be used (see BrianUtils.NeuronModels)
        :param input: str, name of input, that is stored in own NIX File
        :param output: str, name of output, ...
        :param inits: dict, additional initial values for model (see examples in BrianUtils.NeuronModels.AdEx)
        :param popsize: int, population size for optimizing algorithm CMA-ES
        :param maxiter: int, maximum iterations count
        :param algoptparams: dict, optimization parameters of algorithm used
        :param algo: str, algorithm used
        :param from_perc: bool, whether ranges will be calculated from initial values or not. Don't use!
        :param optparams: list, parameters you would want to optimize
        :param returninfo: whether brian will return info ir not (see brian.modelfitting.modelfitting). Don't use!
        :param logstr: str, text for log file, that will be created after fitting
        :return: str, name of fitting and created section in NIX File, in "modelFittings" section
        '''
        self.file.openNixFile()
        si = self.file.GetIn(input)
        sig, spk = self.file.GetOut(output)
        self.file.closeNixFile()
        model_str = str(model)
        model = NM.GetModelById(model_str)
        modelInst = model(inits, from_perc=from_perc)
        print "ModelStr = ",model_str
        print "Optimizing ",
        if not optparams is None:
            modelInst.set_optparams_list(*optparams)
            print optparams
        else: print modelInst.get_optparams_list()
        results, inits = MF.FitSingleCompartmentalModel(modelInst, si, spk,
                                                        popsize=popsize, maxiter=maxiter, algo_params=algoptparams,
                                                        algorithm=algo, returninfo=returninfo)
        ctime = str(dt.datetime.now())
        self.file.openNixFile()
        name = self.file.AddFit(name = ctime, results=results, initials=inits, model = model_str,
                         in_name=input, out_name=output, description="fitting", safe=True, returninfo=returninfo)
        self.file.closeNixFile()
        if not logstr is None:
            f = open(os.path.join(FS.OUTPUT, name), "w")
            f.write(logstr)
            f.close()
        print results.best_pos
        print "initials:", inits
        try:
            pass
        finally:
            self.file.closeNixFile()
        return name

    def SimulateFitting(self, fname):
        '''
        Simulates model with parameters, obtained by modelfitting, that is stored with given name in NIX File.
        Saves simulated traces into same NIX File. Better not to use, it would be too slow to read it afterwards
        :param fname: str, modelFitting name
        :return: None
        '''
        self.file.openNixFile()
        try:
            fitting = self.file.GetFit(fname)
            self.file.closeNixFile()
            if fitting!=None:
                input = self.file.GetIn(fitting["input"])
                model = NM.GetModelById(fitting["model"])
                print fitting["model"], model, type(model)
                inits = fitting["inits"]
                inits.update(fitting["fitted"])
                inp_var = fitting["input_var"]
                time = TimeToBrian(input.t_start)
                duration = TimeToBrian(input.duration)
                sim = S.Simulator(model())
                sim.set_time(time)
                sim.set_input(inp_var, input)
                res = sim.run(duration, dtime = 0.1*S.b.ms, inits=inits)
                self.file.openNixFile()
                self.file.AddSim(fname, res)
        finally:
            self.file.closeNixFile()

    def SimulateAndPlotFitting(self, fname, legend = True, sigfilter = lambda x:True, spkfilter = lambda x:True,
                               savesize = None, savename = None):
        '''
        Use instead of SimulateFitting. Will take parameters from modelfitting, simulate, plot and save as json file.
        :param fname: str, name of fitting
        :param legend: bool, whether to show legend or not
        :param sigfilter: function, decides, which signals would be plotted, and which not
        :param spkfilter: function, decices, which spiketrains to plot and which not
        :param savesize: tuple (x, y). If not None, will save plot as figure with size (x, y) instead of plotting
        :param savename: filename, where to save figure (if savesize is not None)
        :return: None
        '''
        self.file.openNixFile(mode=MIO.nix.FileMode.ReadOnly)
        try:
            fitting = self.file.GetFit(fname)
            if fitting != None:
                self.file.closeNixFile()
                path = os.path.join(FS.TRACES, fname+".plot.json")
                if os.path.exists(path):
                    obj = nio.LoadJson(path)
                    PL.PlotLists([zip(obj[0], obj[1])], sigfilter = sigfilter, spkfilter = spkfilter,
                                 savesize=savesize, savename=savename)
                else:
                    input = self.file.GetIn(fitting["input"])
                    output = self.file.GetOut(fitting["output"])
                    self.file.closeNixFile()
                    model = NM.GetModelById(fitting["model"])
                    print fitting["model"], model, type(model)
                    inits = fitting["inits"]
                    inits.update(fitting["fitted"])
                    inp_var = fitting["input_var"]
                    time = TimeToBrian(input.t_start)
                    duration = TimeToBrian(input.duration)
                    sim = S.Simulator(model())
                    sim.set_time(time)
                    sim.set_input(inp_var, input)
                    res = sim.run(duration, dtime=0.1 * S.b.ms, inits=inits)
                    spks = [None]*len(res)+[output[1]]
                    sigs = res + [output[0]]
                    title = "Fitting {0} for neuron {1}".format(fname, self.file.exp)
                    pltlst = [zip(sigs, spks)]
                    PL.PlotLists(pltlst, legend = legend, title = title, sigfilter = sigfilter, spkfilter = spkfilter,
                                 savesize = savesize, savename=savename)
                    nio.SaveResults(path, sigs, spks)
        finally:
            self.file.closeNixFile()

    def PlotSimulation(self, fname, expsig = False, expspk = False):
        '''
        Plots simutation, provided by SimulateFitting function.
        :param fname: name of simulation (same as fitting name)
        :param expsig: bool, to plot experimental recording signal or not
        :param expspk: bool, to plot experimental spikes or not
        :return: None
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        spks = []
        sigs = []
        try:
            res = self.file.GetSim(fname)
            if expsig or expspk:
                sig, spk = self.file.GetOut(res["output"])
                if expsig: sigs.append(sig)
                else: sigs.append(None)
                if expspk: spks.append(spk)
                else: spks.append(None)
            sigs += res["monitors"]
            spks += [None]*len(res["monitors"])
        finally:
            self.file.closeNixFile()
        title = "Neuron : {0}, fitting : {1}".format(self.file.exp, fname)
        PL.PlotLists([zip(sigs, spks)], title = title)

    def PlotFitness(self, name):
        '''
        Should plot fitness function from fitting
        :param name: str,  name of fitting
        :return: None
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        res = self.file.GetFit(name)
        obj = MIO.pickle.load(open(os.path.join(FS.FITTING, self.file.exp, res["pickle"])))
        arr = obj.result[0][2][0]['best_fitness']
        print arr
        print obj.best_pos
        PL.plt.plot(arr, "bo-")
        PL.plt.xlabel("Iteration number")
        PL.plt.ylabel("Fitness")
        PL.plt.title("Neuron : {0}, fitting : {1}".format(self.file.exp, name))
        PL.plt.show()
        self.file.closeNixFile()

    def PlotStd(self, name):
        '''
        Plots dist_std from fitting
        :param name: fitting name
        :return: None
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        res = self.file.GetFit(name)
        obj = MIO.pickle.load(open(os.path.join(FS.FITTING, self.file.exp, res["pickle"])))
        arr = obj.result[0][2][0]['dist_std']
        print arr
        print obj.best_pos
        PL.plt.plot(arr, "bo-")
        PL.plt.xlabel("Iteration number")
        PL.plt.ylabel("Dist Std")
        PL.plt.title("Neuron : {0}, fitting : {1}".format(self.file.exp, name))
        PL.plt.show()
        self.file.closeNixFile()

    def GetFittingNames(self):
        '''
        Returns fitting names, presented in NIX File
        :return: list of str
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        lst = self.file.GetFitNames()
        self.file.closeNixFile()
        return lst

    def GetInputNames(self):
        '''
        Returns input names, presented in NIX File
        :return: list of str
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        lst = self.file.GetInNames()
        self.file.closeNixFile()
        return lst

    def GetOutputNames(self):
        '''
        Returns output names, presented in NIX File
        :return: list of str
        '''
        self.file.openNixFile(MIO.nix.FileMode.ReadOnly)
        lst = self.file.GetOutNames()
        self.file.closeNixFile()
        return lst

    def PlotInput(self, name):
        '''
        Plots input, stored in NIX File, by given name
        :param name: name of input
        :return: None
        '''
        inp = self.file.GetIn(name)
        PL.PlotLists([[inp, None]])