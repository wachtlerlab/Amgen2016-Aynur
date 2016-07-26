from brian_test import simulation as sim, NeuronModels as NM
from sig_proc import multiple as mp, plot as pt, signals as sg
import quantities as q

blk = mp.ReadExperiment("130605-2LY")

input = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1" and f.description=="Current"]

simul = sim.Simulator(NM.AdEx())

print input

simul.set_input("I", input[0])

res = simul.run(time=1*q.s, dtime=0.02*q.ms)

mp.PlotSets(res)