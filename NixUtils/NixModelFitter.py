from BrianUtils import ModelFitter as MF
from BrianUtils import NeuronModels as NM
from BrianUtils import Simulator as S
from BrianUtils.Utilities import TimeToBrian
from NixUtils import ModelfittingIO as MIO
from NixUtils import ProjectFileStructure as FS
from NeoUtils import NeoPlot as PL
import datetime as dt

class NixModelFitter(object):
    def __init__(self, expname):
        self.file = MIO.ModelfittingIO(expname, FS.FITTING)
        self.file.closeNixFile()

    def FitSomething(self, model, input, output, popsize=1000, maxiter=2):
        self.file.openNixFile()
        si = self.file.GetIn(input)
        sig, spk = self.file.GetOut(output)
        model_str = str(model)
        print "ModelStr = ",model_str
        model = NM.GetModelById(model_str)
        results, inits = MF.FitModel(model(), si, spk, popsize=popsize, maxiter=maxiter)
        ctime = str(dt.datetime.now())
        self.file.AddFit(name = ctime, results=results, initials=inits, model = model_str,
                         in_name=input, out_name=output, description="fitting", safe=True)
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
        res = self.file.GetSim(fname)
        spks = []
        sigs = []
        if expsig or expspk:
            sigs, spks = self.file.GetOut(res["output"])
        sigs += res["monitors"]
        PL.PlotSets(sigs, spks)

    def GetFittingNames(self):
        self.file.openNixFile()
        lst = self.file.GetFitNames()
        self.file.closeNixFile()
        return lst
