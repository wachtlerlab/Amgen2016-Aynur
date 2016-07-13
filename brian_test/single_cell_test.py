import SYM, numpy as np
from M import ms, mA, uA, mV, defaultclock

defaultclock.dt=0.01*ms


timemax = 100
seq = np.arange(10980, timemax-15, 2)
spk = zip([0]*len(seq), [i*ms for i in seq])

inits = {'V' : 0*mV, 'I' : 31*uA}

time = timemax*ms


myModel = SYM.M.AdEx()

for i in [33]:
    defaultclock.t=0*ms
    dV = i*mV
    SYM.single_cell(myModel, time=time, inits=inits,
                    spikes = spk, dV= dV)





SYM.M.legend()
SYM.M.xlabel("time, ms")
SYM.M.ylabel("value, unit")
SYM.M.show()