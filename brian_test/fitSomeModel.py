from brian.library import modelfitting as m
import brian
import time
import quantities as q

def FitModel(NModel, input, output, popsize = 1000, maxiter = 100, dt = 0.02, cpu = 2, gpu = 0, method = "RK"):
    def printm(**kwargs):
        print kwargs
    t_prev = time.time()
    di = NModel.get_opt_params()
    input_raw = brian.TimedArray(input.signal, input.times)
    deltaT = dt*q.ms
    result =  m.modelfitting(NModel.get_model(), NModel.get_reset(), NModel.get_threshold(),
                          data = output, input_var = input.var, input = input_raw,
                          dt = deltaT, popsize=popsize,
                          maxiter = maxiter, initial_values=NModel.get_inits(),
                          cpu = cpu, gpu = gpu, method = method, **di
                          )
    t_next = time.time()
    return result, t_next-t_prev