from brian.library import modelfitting as m
import brian
import time

import sig_proc.signals

def FitModel(NModel, input, output, popsize = 10000, maxiter = 100, dt = 0.02, method = "RK"):
    t_prev = time.time()
    di = NModel.get_opt_params()
    input_raw = sig_proc.signals.TimedArray_from_AnalogSignal(input)

    deltaT = dt*brian.ms
    result =  m.modelfitting(NModel.get_model(), NModel.get_reset(), NModel.get_threshold(),
                          data = output, input_var = input.var, input = input_raw,
                          dt = deltaT, popsize=popsize,
                          maxiter = maxiter, initial_values=NModel.get_inits(),
                          method = method, returninfo=True,
                        **di
                          )
    t_next = time.time()
    return result, t_next-t_prev