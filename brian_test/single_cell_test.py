from brian_test import SYM
import numpy as np
from brian_test.M import ms, mA, nA, uA, mV, defaultclock, nS, pF, TimedArray
import input_signals as I



defaultclock.dt=0.02*ms

timemax = 100
dtstep = 0.02

seq = np.arange(18900, timemax-15, 5)
spk = zip([0]*len(seq), [i*ms for i in seq])

X = I.gen_time_interval(0, timemax, dtstep)
Y = I.gen_constant_signal(X, 1)
Y = I.PeriodicRectFilter(50, 40, 0).on(X, Y)
#Y = I.SingleRectFilter(10 , 50).on(X, Y)
Y = I.VolFilter(3).on(X, Y)


def run_single_test(model, inits):
    initials = {'I' : I.TR(Y, nA, dtstep, ms)} #, 'tau': 20*ms, 'C':600*pF, 'gL': 30*nS, 'a': 6*nS}

    initials.update(inits)
    time = timemax*ms

    myModel = model(initials)

    for i in [41]:
        defaultclock.t=0*ms
        dV = i*mV
        SYM.single_cell(myModel, time=time,
                        spikes = spk, dV= dV, monitors={"V":mV, "I":nA})

    SYM.M.legend()
    SYM.M.xlabel("time, ms")
    SYM.M.ylabel("value, unit")
    SYM.M.show()

def run_custom_single_test(model, inits, start, time, dt):
    initials = {'I' : I.TR(Y, nA, dtstep, ms)} #, 'tau': 20*ms, 'C':600*pF, 'gL': 30*nS, 'a': 6*nS}

    initials.update(inits)

    myModel = model(initials)

    defaultclock.t= start
    defaultclock.dt = dt

    SYM.single_cell(myModel, time=time, monitors={"V":mV, "I":nA})

    SYM.M.legend()
    SYM.M.xlabel("time, ms")
    SYM.M.ylabel("value, unit")
    SYM.M.show()