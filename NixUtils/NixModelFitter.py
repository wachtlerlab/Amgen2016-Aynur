from BrianUtils import ModelFitter as MF
from BrianUtils import NeuronModels as NM
from BrianUtils import Simulator as S
from BrianUtils.Utilities import TimeToBrian
from NixUtils import ModelfittingIO as MIO
from NixUtils import ProjectFileStructure as FS
from NeoUtils import NeoPlot as PL
import datetime as dt
import os

class NixModelFitter(object):
    def __init__(self, expname):
        self.file = MIO.ModelfittingIO(expname, FS.FITTING)
        self.file.closeNixFile()

    def FitSomething(self, model, input, output, inits = {}, popsize=1000, maxiter=100, algoptparams = {}, algo ="CMAES",
                     from_perc = True, optparams = None):
        self.file.openNixFile()
        si = self.file.GetIn(input)
        sig, spk = self.file.GetOut(output)
        model_str = str(model)
        print "ModelStr = ",model_str
        model = NM.GetModelById(model_str)
        modelInst = model(inits, from_perc=from_perc)
        if not optparams is None:
            modelInst.set_opt_params(optparams)
        results, inits = MF.FitModel(modelInst, si, spk,
                                     popsize=popsize, maxiter=maxiter, algo_params=algoptparams,
                                     algorithm=algo)
        ctime = str(dt.datetime.now())
        self.file.AddFit(name = ctime, results=results, initials=inits, model = model_str,
                         in_name=input, out_name=output, description="fitting", safe=True)
        print results.best_pos
        print "initials:", inits
        try:
            pass
        finally:
            self.file.closeNixFile()

    def SimulateFitting(self, fname):
        self.file.openNixFile()
        try:
            fitting = self.file.GetFit(fname)
            if fitting!=None:
                input = self.file.GetIn(fitting["input"])
                model = NM.GetModelById(fitting["model"])
                print fitting["model"], model, type(model)
                inits = fitting["inits"]
                inp_var = fitting["input_var"]
                time = TimeToBrian(input.t_start)
                duration = TimeToBrian(input.duration)
                sim = S.Simulator(model())
                sim.set_time(time)
                sim.set_input(inp_var, input)
                res = sim.run(duration, inits=inits)
                self.file.AddSim(fname, res)
        finally:
            self.file.closeNixFile()

    def PlotSimulation(self, fname, expsig = False, expspk = False):
        self.file.openNixFile()
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
        self.file.openNixFile()
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

    def GetFittingNames(self):
        self.file.openNixFile()
        lst = self.file.GetFitNames()
        self.file.closeNixFile()
        return lst

    def GetInputNames(self):
        self.file.openNixFile()
        lst = self.file.GetInNames()
        self.file.closeNixFile()
        return lst

    def GetOutputNames(self):
        self.file.openNixFile()
        lst = self.file.GetOutNames()
        self.file.closeNixFile()
        return lst

    def PlotInput(self, name):
        inp = self.file.GetIn(name)
        PL.PlotLists([[inp, None]])