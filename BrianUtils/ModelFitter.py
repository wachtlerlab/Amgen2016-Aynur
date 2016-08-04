from brian.library import modelfitting as m
import brian


def FitModel(NModel, input, output, popsize=10000, maxiter=100, method="RK"):

    input_raw = input.simplified.magnitude
    output_spk = output.times

    model = NModel.get_model()
    reset = NModel.get_reset()
    threshold = NModel.get_threshold()
    opt_params = NModel.get_opt_params()
    input_dt = float(input.sampling_period.simplified.magnitude)*brian.second
    initial_params = NModel.get_inits()

    result = m.modelfitting(model, reset, threshold,
                            data=output_spk, input_var="I", input=input_raw,
                            dt = input_dt, popsize=popsize,
                            maxiter=maxiter, initial_values=initial_params,
                            method=method, returninfo=True, algorithm=m.CMAES,
                            **opt_params
                            )
    return result, initial_params

def Print(results):
    m.print_table(results)