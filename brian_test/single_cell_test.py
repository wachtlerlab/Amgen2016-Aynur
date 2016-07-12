import SYM

SYM.M.defaultclock.dt=0.01*SYM.M.ms

spk = []

def funcI(time):
    if time < 140*SYM.M.ms and time > 14*SYM.M.ms:
        return 15*SYM.M.uA

inits = {'V' : 0*SYM.M.mvolt, 'I' : 0*SYM.M.uA}

mons = {"V":SYM.M.mV, "INa":10*SYM.M.uA, "IK":10*SYM.M.uA, "Il":10*SYM.M.uA, "I":10*SYM.M.uA}

time = 150*SYM.M.msecond



for i in [30]:
    SYM.M.defaultclock.t=0*SYM.M.ms
    dV = i*SYM.M.mvolt
    SYM.single_cell(SYM.M.hodjkin_huxley(), time=time, initials=inits,
                    spikes = spk, monitors = mons, deltaV = -dV)


SYM.M.legend()
SYM.M.show()