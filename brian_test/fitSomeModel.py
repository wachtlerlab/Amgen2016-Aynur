import M
from brian.library import modelfitting as m

def FitModel(NModel, input, output, popsize = 1000, maxiter = 100, dt = 0.1, cpu = 2, gpu = 0, method = "RK"):
    return m.modelfitting(NModel.get_model(), NModel.get_reset(), NModel.get_threshold(),
                          data = output, input_var = input.var, input = input.signal, dt = dt, popsize=popsize,
                          maxiter = maxiter, initial_values=NModel.get_inits(), cpu = cpu, gpu = gpu
                          )
