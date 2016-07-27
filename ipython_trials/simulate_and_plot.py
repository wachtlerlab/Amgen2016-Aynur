from brian_test import simulation as sim, NeuronModels as NM
from sig_proc import multiple as mp, plot as pt, signals as sg
import quantities as q
import brian as b

blk = mp.ReadExperiment("130605-2LY")

input = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1" and f.description=="current"]

output = []#[f for f in blk.segments[0].analogsignals if "Trial"in f.name and f.description=="voltage"]

spikes = [f for f in blk.segments[0].spiketrains if "Trial" in f.name]

simul = sim.Simulator(NM.AdEx())

duration = 0.2*b.second

print "INPUT:", input

currInput = sg.ShiftSignalNull(input[0], 50*q.ms)
currInput = currInput[currInput.times<duration]

for i in xrange(len(output)):
    output[i] = sg.ShiftSignalNull(output[i], 50*q.ms)
    output[i] = output[i][output[i].times < duration]

for i in xrange(len(spikes)):
    spikes[i] = sg.ShiftSpikeTrain(spikes[i], 50*q.ms)
    spikes[i] = spikes[i][spikes[i].times < duration]

simul.set_input("I", currInput)

myMonitors = {"I": 100*b.mA, "V": b.mV}

res = simul.run(time=duration, dtime=0.05*b.ms, monitors=myMonitors, inits={"scaleFactor":0.000000001})

res = res+output
mp.PlotSets(res, spikes)