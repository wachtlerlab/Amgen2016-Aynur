import numpy as np

import input_signals as I
from brian_projects.NeuronModels.M import ms, nA, mV, defaultclock
from brian_projects.NeuronModels.simulation import SYM

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

    brian_test.NeuronModels.M.legend()
    brian_test.NeuronModels.M.xlabel("time, ms")
    brian_test.NeuronModels.M.ylabel("value, unit")
    brian_test.NeuronModels.M.show()

def run_custom_single_test(model, inits, start, time, dt):
    initials = {'I' : I.TR(Y, nA, dtstep, ms)} #, 'tau': 20*ms, 'C':600*pF, 'gL': 30*nS, 'a': 6*nS}

    initials.update(inits)

    myModel = model(initials)

    defaultclock.t= start
    defaultclock.dt = dt

    SYM.single_cell(myModel, time=time, monitors={"V":mV, "I":nA})

    brian_test.NeuronModels.M.legend()
    brian_test.NeuronModels.M.xlabel("time, ms")
    brian_test.NeuronModels.M.ylabel("value, unit")
    brian_test.NeuronModels.M.show()

def return_custom_single_test(model, inits, start, time, dt):
    initials = {'I' : I.TR(Y, nA, dtstep, ms)} #, 'tau': 20*ms, 'C':600*pF, 'gL': 30*nS, 'a': 6*nS}

    initials.update(inits)

    myModel = model(initials)

    defaultclock.t= start
    defaultclock.dt = dt

    return SYM.single_cell_return(myModel, time=time, monitors={"V":mV, "I":nA})

if __name__=="__main__":
    run_custom_single_test(brian_test.NeuronModels.M.AdEx, inits = {}, start =0 * ms, time =timemax * ms, dt =dtstep * ms)