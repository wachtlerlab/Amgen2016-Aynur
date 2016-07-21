import neo
import numpy as np
import quantities as q
import signals.plot as pl
x = np.arange(-2, 10, 0.1)
y1 = np.sin(x)*q.mA
y2 = np.cos(x)*q.uA
sig1 = neo.AnalogSignal(y1, t_start = x[0]*q.s, sampling_period=(x[1]-x[0])*q.s, units = "mA")
sig2 = neo.AnalogSignal(y2, t_start = x[0]*q.s, sampling_period=(x[1]-x[0])*q.s, units = "mA")


pl.plot_single_analog_signal(sig1)
pl.plot_single_analog_signal(sig2)
pl.show()