import SYM
SYM.M.defaultclock.dt=0.01*SYM.M.ms

spk = [(0, i*SYM.M.ms) for i in xrange(4, 120)]

inits = {'V' : 0*SYM.M.mvolt, 'I' : 0*SYM.M.uA}

mons = {"V":SYM.M.mV, "INa":10*SYM.M.uA, "IK":10*SYM.M.uA, "Il":10*SYM.M.uA, "I":10*SYM.M.uA}

time = 150*SYM.M.msecond

spkp = "I"

units = {"V":SYM.M.mvolt, "I":SYM.M.uA}

for i in [30]:
    SYM.M.defaultclock.t=0*SYM.M.ms
    dV = i*units[spkp]
    SYM.single_cell(SYM.M.hodjkin_huxley(), time=time, initials=inits,
                    spikes = spk, sptype=spkp, monitors = mons, deltaV = -dV,
                    prefix="$dV={0}mV$, ".format(i))


SYM.M.legend()
SYM.M.show()