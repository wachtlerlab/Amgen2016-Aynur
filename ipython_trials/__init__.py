from brian_test import simulation as sim, NeuronModels as NM
from sig_proc import multiple as mp, plot as pt, signals as sg
import quantities as q
import brian as b

blk = mp.ReadExperiment("130605-2LY")

input = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1" and f.description=="Current"]

simul = sim.Simulator(NM.AdEx())

print "INPUT:", input

currInput = sg.ShiftSignalNull(input[0], 10*q.ms)

simul.set_input("I", currInput)

myMonitors = {"i": b.nA, "V": b.mV}

res = simul.run(time=0.2*b.second, dtime=0.02*b.ms, monitors=myMonitors, inits={"scaleFactor":0.00000001})

# res.append(input[0])
mp.PlotSets(res)