import SYM, numpy as np

SYM.M.defaultclock.dt=0.01*SYM.M.ms


timemax = 100
seq = np.arange(10, timemax-15, 25)
spk = zip([0]*len(seq), [i*SYM.M.ms for i in seq])

def funcI(time):
    if time < 140*SYM.M.ms and time > 14*SYM.M.ms:
        return 0*SYM.M.uA

inits = {'V' : 0*SYM.M.mvolt, 'I' : 0*SYM.M.uA}

mons = {"V":SYM.M.mV, "INa":10*SYM.M.uA, "IK":10*SYM.M.uA, "Il":10*SYM.M.uA, "I":10*SYM.M.uA}

time = timemax*SYM.M.msecond



for i in [3]:
    SYM.M.defaultclock.t=0*SYM.M.ms
    dV = i*SYM.M.mvolt
    SYM.single_cell(SYM.M.hodgkin_huxley(), time=time, initials=inits,
                    spikes = spk, monitors = mons, deltaV = -dV)


SYM.M.legend()
SYM.M.xlabel("time, ms")
SYM.M.ylabel("value, unit")
SYM.M.show()