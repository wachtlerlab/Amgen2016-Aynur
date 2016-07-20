from brian.library import modelfitting as m
import brian
import time

def FitModel(NModel, input, output, popsize = 1000, maxiter = 100, dt = 0.02, method = "RK"):
    t_prev = time.time()
    di = NModel.get_opt_params()
    input_raw = brian.TimedArray(arr=input.signal, times=input.times)
    deltaT = dt*brian.ms
    result =  m.modelfitting(NModel.get_model(), NModel.get_reset(), NModel.get_threshold(),
                          data = output, input_var = input.var, input = input_raw,
                          dt = deltaT, popsize=popsize,
                          maxiter = maxiter, initial_values=NModel.get_inits(),
                          method = method, **di
                          )
    t_next = time.time()
    return result, t_next-t_prev