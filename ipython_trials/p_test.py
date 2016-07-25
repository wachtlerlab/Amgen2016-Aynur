import sig_proc as ss
import quantities as q
blk = ss.multiple.ReadExperiment("130605-2LY")
# ss.multiple.PlotExperiment(blk, subplots=False)


spksl = blk.segments[0].spiketrains
sg = blk.segments[0].analogsignals[0]

ss.plot.subplot(1, 2, 1)
for s in spksl:
    color = ss.plot.__plot_single_analog_signal(sg)
    ss.plot.__plot_single_spike_train(s, color)

ss.plot.subplot(1, 2, 2)
spks = ss.signals.JoinSpikeTrainsShifted(spksl, 2*q.s)
ss.plot.__plot_single_spike_train(spks)
ss.plot.show()