import neo
import numpy as np
import quantities as q
import sig_proc.plot as pl
import sig_proc.signals

x = np.arange(-2, 10, 0.1)
y1 = np.sin(x)*q.mA
y2 = np.cos(x)*q.uA
print x
sig1 = neo.AnalogSignal(y1, t_start = x[0]*q.s, sampling_period=(x[1]-x[0])*q.s, units = "mA")
sig21 = neo.AnalogSignal(y1, t_start = x[-1]*q.s, sampling_period=(x[1]-x[0])*q.s, units = "mA")
sig2 = neo.AnalogSignal(y2, t_start = x[0]*q.s, sampling_period=(x[1]-x[0])*q.s, units = "uA")
sig3 = neo.AnalogSignal(y2, t_start = x[0]*q.s, sampling_period=(x[2]-x[0])*q.s, units = "A")

sig4 = neo.IrregularlySampledSignal(x*q.s, y1, units = "mA")

pl.subplot(1, 3, 1)
pl.__plot_single_analog_signal(sig1, timeunit=q.s)
pl.subplot(1, 3, 2)
pl.__plot_single_analog_signal(sig21, timeunit=q.s)
pl.subplot(1, 3, 3)
pl.__plot_single_analog_signal(sig_proc.signals.Concat(sig1, sig21), timeunit=q.s)

pl.show()
