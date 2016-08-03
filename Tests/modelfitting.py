import quantities as q

import NixUtils.ModelfittingIO
import NeoUtils as sp
from BrianUtils import NeuronModels as NM
from BrianUtils import ModelFitter as Ft
from BrianUtils.Utilities import timer

expName = "130322-1LY"
t = timer()
exp = NixUtils.ModelfittingIO.ReadExperiment(expName)
t.record()
spks = exp.segments[0].spiketrains
sigs = [sig for sig in exp.segments[0].analogsignals if sig.name=="PredictedInput1" and sig.description=="current"]*len(spks)
shift = sp.Signals.NearestDivident(2 * q.s, sigs[0].sampling_period)
ishift = shift
input = sp.Signals.ShiftSignalNull(sp.Signals.Join_Shifted(sigs, shift), ishift)
output = sp.Signals.ShiftSpikeTrain(sp.Signals.JoinSpikeTrainsShifted(spks, shift), ishift)

model = NM.Models.AdEx()
t.record()
results, inits = Ft.FitModel(model, input=input, output=output, popsize=1000, maxiter=5)
t.record()
Ft.Print(results)
print "timing:", t.flush()
print inits


