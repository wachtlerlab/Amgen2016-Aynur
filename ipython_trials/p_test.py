import sig_proc as ss
import quantities as q
blk = ss.multiple.ReadExperiment("130605-2LY")
# ss.multiple.PlotExperiment(blk, subplots=False)

sgl = blk.segments[0].analogsignals
n = int(2*q.s/sgl[0].sampling_period)
time = sgl[0].sampling_period*n
sg = ss.signals.Join_Shifted(sgl, dtime = time)
spksl = blk.segments[0].spiketrains
spks = ss.signals.JoinSpikeTrainsShifted(spksl, dtime = time)
ss.plot.subplot(1, 2, 1)
ss.plot.__plot_single_analog_signal(sgl[-1])
ss.plot.__plot_single_spike_train(spksl[-1])
ss.plot.subplot(1, 2, 2)
ss.plot.__plot_single_analog_signal(sg)
ss.plot.__plot_single_spike_train(spks)
ss.plot.show()