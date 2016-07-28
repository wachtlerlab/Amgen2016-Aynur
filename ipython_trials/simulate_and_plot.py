from brian_test import simulation as sim, NeuronModels as NM
from sig_proc import multiple as mp, plot as pt, signals as sg
import quantities as q
import brian as b

blk = mp.ReadExperiment("130322-1LY")

input = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1-1" and f.description=="current"]

voltage = [f for f in blk.segments[0].analogsignals if f.name=="PredictedInput1" and f.description=="voltage"]

output = []#[f for f in blk.segments[0].analogsignals if "Trial"in f.name and f.description=="voltage"]

spikes = []#[f for f in blk.segments[0].spiketrains if "Trial" in f.name]

simul = sim.Simulator(NM.AdEx())

duration = 0.6*b.second

print "INPUT:", input

initials = {
    "scaleFactor": 0.1,
    # "a":   20 * b.nS,
}

'''ad_ex_custom_fitting1 = {
    "Vr": -70.6 * mV,  # -48.5*mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -70.4 * mV,
    "sF": 2 * mV,
    "tau": 144 * ms,
    "EL": -70.6 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 4 * nS,
    "Vp": 20 * mV
}'''

#initials.update(ad_ex_custom_fitting1)

shift = 300*q.ms
inp_duration = 250*q.ms

currInput = sg.ShiftSignalNull(input[0], shift)
currInput = currInput[currInput.times<duration]

currInput = sg.SignalBuilder(currInput).get_rect(shift, shift+inp_duration, amplitude=8*q.nA)

voltage = sg.ShiftSignal(voltage[0], shift)

for i in xrange(len(output)):
    output[i] = sg.ShiftSignalNull(output[i], shift)
    output[i] = output[i][output[i].times < duration]

for i in xrange(len(spikes)):
    spikes[i] = sg.ShiftSpikeTrain(spikes[i], shift)
    spikes[i] = spikes[i][spikes[i].times.simplified < duration]

simul.set_input("I", currInput)

myMonitors = {
    "I": b.nA,
    "V": b.mV,
    "w": 1000*b.nA,
    "Ex":1000*b.mA
}

'''myMonitors.update({
            "w":   1 * b.nA,
            "Ex":  1 * b.nA,
            "Vr": 10 * b.mV,
            "Vt": 10 * b.mV,
            "b":0.01 * b.nA,
            "sF":  1 * b.mV,
            "tau":10 * b.ms,
            "EL": 10 * b.mV,
            "gL": 10 * b.nS,
            "C":  50 * b.pF,
            "a":   1 * b.nS,
            "Vp":  5 * b.mV,
            # "Ex":  1 * b.nA
        })'''

initials.update({})

res = simul.run(time=duration, dtime=0.02*b.ms, monitors=myMonitors, inits=initials)

res = res#+output[voltage]

mp.PlotSets(res, spikes)