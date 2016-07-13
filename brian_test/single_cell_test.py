import SYM, numpy as np
from M import ms, mA, nA, uA, mV, defaultclock, nS, pF, TimedArray
import input_signals as I

defaultclock.dt=0.01*ms

timemax = 100
dtstep = 0.1

seq = np.arange(10234, timemax-15, 2)
spk = zip([0]*len(seq), [i*ms for i in seq])

X = I.gen_time_interval(0, timemax, dtstep)
Y = I.gen_constant_signal(X, 1)
print Y
Y = I.PeriodicSineFilter(15, 0).on(X, Y)
print Y
Y = I.VolFilter(9).on(X, Y)

inits = {'I' : I.TR(Y, uA, dtstep, ms)}

time = timemax*ms


myModel = SYM.M.hodgkin_huxley(inits)

for i in [0]:
    defaultclock.t=0*ms
    dV = i*mV
    SYM.single_cell(myModel, time=time,
                    spikes = spk, dV= dV, monitors={"V":mV, "I":uA})





SYM.M.legend()
SYM.M.xlabel("time, ms")
SYM.M.ylabel("value, unit")
SYM.M.show()