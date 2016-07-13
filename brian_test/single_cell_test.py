import SYM, numpy as np
from M import ms, mA, nA, uA, mV, defaultclock, nS, pF, TimedArray
import input_signals as I

defaultclock.dt=0.01*ms

timemax = 50
dtstep = 1.

seq = np.arange(10980, timemax-15, 2)
spk = zip([0]*len(seq), [i*ms for i in seq])

X = I.gen_time_interval(0*ms, timemax*ms, dtstep*ms)
print X
Y = I.gen_constant_signal(X, 1*uA)
print Y
Y = I.QuadraticFilter(10, 30).on(X, Y)
print Y

inits = {'I' : I.TR(Y, dtstep*ms), 'tau': 20*ms, 'C':600*pF, 'gL': 30*nS, 'a': 6*nS}

time = timemax*ms


myModel = SYM.M.AdEx(inits=inits)

for i in [13]:
    defaultclock.t=0*ms
    dV = i*mV
    SYM.single_cell(myModel, time=time,
                    spikes = spk, dV= dV)





SYM.M.legend()
SYM.M.xlabel("time, ms")
SYM.M.ylabel("value, unit")
SYM.M.show()