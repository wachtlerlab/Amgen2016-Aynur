from BrianUtils import ModelFitter as MF
from NixUtils import ModelfittingIO as MIO
from NixUtils import ProjectFileStructure as FS
from BrianUtils import NeuronModels as NM
from BrianUtils import Simulator as S
from BrianUtils.Utilities import TimeToBrian
from NeoUtils.NeoJsonIO import SaveResults
import datetime as dt

class NixModelFitter(object):
    def __init__(self, expname):
        self.file = MIO.ModelfittingIO(expname, FS.FITTING)
        self.file.close()

    def FitSomething(self, model, input, output, popsize=1000, maxiter=2):
        self.file.open()
        si = self.file.get_input(input)
        sig, spk = self.file.get_output(output)
        model_str = str(model)
        print "ModelStr = ",model_str
        model = NM.GetModelById(model_str)
        results, inits = MF.FitModel(model(), si, spk, popsize=popsize, maxiter=maxiter)
        ctime = str(dt.datetime.now())
        self.file.add_fitting(name = ctime, results=results, initials=inits, model = model_str,
                              in_name=input, out_name=output, description="fitting", safe=True)
        try:
            pass
        finally:
            self.file.close()

    def SimulateFitting(self, fname):
        self.file.open()
        res = ([], [])
        try:
            fitting = self.file.get_fitting(fname)
            if fitting!=None:
                input = self.file.get_input(fitting["input"])
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
                out_sig, out_spks = self.file.get_output(fitting["output"])
                SaveResults(FS.os.path.join(FS.os.path.expanduser("~"), fname+".json"), res, [])
        finally:
            self.file.close()


    def GetFittingNames(self):
        self.file.open()
        lst = self.file.get_fitting_names()
        self.file.close()
        return lst
