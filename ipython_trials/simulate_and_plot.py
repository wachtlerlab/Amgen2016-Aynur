import numpy as np

import brian as b
import quantities as q

import brian_test.Simulator
from brian_test import NeuronModels as NM
from sig_proc import multiple as mp, signals as sg

blk = mp.ReadExperiment("130322-1LY")

input = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1-1" and f.description=="current"]
# voltage = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1" and f.description=="voltage"]
output = []#[f for f in blk.segments[0].analogsignals if "Trial"in f.name and f.description=="voltage"]
spikes = []# [f for f in blk.segments[0].spiketrains if "Trial" in f.name]

model = NM.AdEx()
simul = brian_test.Simulator.Simulator(model)

duration = 1.1*b.second
shift = 200*q.ms
inp_duration = 800*q.ms
n_shift = 400*q.ms

initials = {
    "scaleFactor": 1.,
}

initials.update(model.bursting_rebound)
def func(times):
    k = times > shift+n_shift
    print k
    tlen= len(times)
    llen = len(times[k])
    return np.array([1.]*(tlen-llen)+[-1.]*llen)

currInput = sg.ShiftSignalNull(input[0], shift)
currInput = currInput[currInput.times<duration]
template = sg.SignalBuilder(currInput)
currInput = template.get_rect(shift, shift+inp_duration, amplitude=.8*q.nA)
currInput*= template.get_signal_by_func(func, amplitude=1*q.dimensionless)
# voltage = sg.ShiftSignal(voltage[0], shift)

for i in xrange(len(output)):
    output[i] = sg.ShiftSignalNull(output[i], shift)
    output[i] = output[i][output[i].times < duration]
for i in xrange(len(spikes)):
    spikes[i] = sg.ShiftSpikeTrain(spikes[i], shift)
    spikes[i] = spikes[i][spikes[i].times.simplified < duration]

simul.set_input("I", currInput)

myMonitors = {
    "I": 0.1*b.nA,
    "V": b.mV,
    "w": 0.1*b.nA,
    "Ex":100*b.nA
}

# myMonitors.update({
#             "w":   1 * b.nA,
#             "Ex":  1 * b.nA,
#             "Vr": 10 * b.mV,
#             "Vt": 10 * b.mV,
#             "b":0.01 * b.nA,
#             "sF":  1 * b.mV,
#             "tau":10 * b.ms,
#             "EL": 10 * b.mV,
#             "gL": 10 * b.nS,
#             "C":  50 * b.pF,
#             "a":   1 * b.nS,
#             "Vp":  5 * b.mV,
#             # "Ex":  1 * b.nA
#         })

res = simul.run(time=duration, dtime=0.05*b.ms, monitors=myMonitors, inits=initials)

mp.PlotSets(res, spikes)