import sig_proc as ss
import quantities as q
blk = ss.multiple.ReadExperiment("130605-2LY")
# ss.multiple.PlotExperiment(blk, subplots=False)

sgl = [f for f in blk.segments[0].analogsignals if f.description=="voltage" and "Trial" in f.name]
n = int(2*q.s/sgl[0].sampling_period)
time = sgl[0].sampling_period*n
sg = ss.signals.Join_Shifted(sgl, dtime = time, name="V", description="voltage during exp")
spksl = blk.segments[0].spiketrains
spks = ss.signals.JoinSpikeTrainsShifted(spksl, dtime = time)
ss.multiple.PlotSets([sg], [spks])