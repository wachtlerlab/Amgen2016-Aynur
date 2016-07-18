from brian_test import SYM
import numpy as np
from brian_test.M import ms, mA, nA, uA, mV, defaultclock, nS, pF, TimedArray
import input_signals as I

defaultclock.dt=0.02*ms

timemax = 50
dtstep = 0.02

seq = np.arange(10, timemax-15, 50)
spk = zip([0]*len(seq), [i*ms for i in seq])

#X = I.gen_time_interval(0, timemax, dtstep)
#Y = I.gen_constant_signal(X, 1)
#Y = I.PeriodicRectFilter(17 ,1, 0).on(X, Y)
#Y = I.VolFilter(-8).on(X, Y)

inits = {}#{'I' : I.TR(Y, uA, dtstep, ms)}

time = timemax*ms


myModel = SYM.M.hodgkin_huxley(inits)

for i in [-10]:
    defaultclock.t=0*ms
    dV = i*mV
    SYM.single_cell(myModel, time=time,
                    spikes = spk, dV= dV, monitors={"V":mV, "INa":10*uA, "IK":10*uA, "Il":10*uA})





SYM.M.legend()
SYM.M.xlabel("time, ms")
SYM.M.ylabel("value, unit")
SYM.M.show()