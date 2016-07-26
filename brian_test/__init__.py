import Fitting as Ft
import NeuronModels as NM
import sig_proc as sp
import quantities as q
from brian_test.utilities import timer

def OurFit(expName):
    t = timer()
    exp = sp.multiple.ReadExperiment(expName)
    t.record()
    # sp.multiple.PlotExperiment(exp)
    spks = exp.segments[0].spiketrains
    sigs = [sig for sig in exp.segments[0].analogsignals if sig.name=="PredictedInput1" and sig.description=="Current"]*len(spks)
    shift = sp.signals.nearest_multiple(2*q.s, sigs[0].sampling_period)
    unshifted = sp.signals.Join_Shifted(sigs, shift)
    ishift = shift
    nullsig = sp.signals.get_signal(unshifted.sampling_period, 0*q.s, ishift)
    input = sp.signals.Join_Shifted([nullsig, unshifted], ishift)
    output = sp.signals.ShiftSpikeTrain(sp.signals.JoinSpikeTrainsShifted(spks, shift), ishift)
    print "input:", input.times
    print "output", output.times

    model = NM.Models.AdEx()
    t.record()
    results = Ft.FitModel(model, input=input, output=output, popsize=30, maxiter=5)
    t.record()
    Ft.Print(results)
    print t.flush()

if __name__=="__main__":
    OurFit("130322-1LY")