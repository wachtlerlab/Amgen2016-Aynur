from brian_test import Fitting.ModelFitter as Ft, NeuronModels as NM
import sig_proc as sp
import quantities as q
from brian_test.utilities import timer

def OurFit(expName):
    t = timer()
    exp = sp.multiple.ReadExperiment(expName)
    t.record()
    spks = exp.segments[0].spiketrains
    sigs = [sig for sig in exp.segments[0].analogsignals if sig.name=="PredictedInput1" and sig.description=="current"]*len(spks)
    shift = sp.signals.nearest_multiple(2*q.s, sigs[0].sampling_period)
    ishift = shift
    input = sp.signals.ShiftSignalNull(sp.signals.Join_Shifted(sigs, shift), ishift)
    output = sp.signals.ShiftSpikeTrain(sp.signals.JoinSpikeTrainsShifted(spks, shift), ishift)

    model = NM.Models.AdEx()
    t.record()
    results = Ft.FitModel(model, input=input, output=output, popsize=1000, maxiter=5)
    t.record()
    Ft.Print(results)
    print "timing:", t.flush()

if __name__=="__main__":
    OurFit("130322-1LY")