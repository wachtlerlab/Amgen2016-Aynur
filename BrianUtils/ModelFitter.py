from brian.library import modelfitting as m
import brian


def FitModel(NModel, input, output, popsize=10000, maxiter=100, method="RK", algorithm = "CMAES", algo_params = None):

    input_raw = list(input.simplified.magnitude)
    output_spk = [brian.second*k for k in list(output.times.simplified.magnitude)]
    input_dt = float(input.sampling_period.simplified.magnitude)*brian.second

    algo = {"CMAES":m.CMAES,
            "PSO":m.PSO,
            "GA":m.GA}

    algo_in = algo.get(algorithm)
    if algo_in is None: algo_in = m.CMAES

    model = NModel.get_model()
    reset = NModel.get_reset()
    threshold = NModel.get_threshold()
    opt_params = NModel.get_opt_params()
    initial_params = NModel.get_inits()

    result = m.modelfitting(model, reset, threshold,
                            data=output_spk, input_var="I", input=input_raw,
                            dt = input_dt, popsize=popsize,
                            maxiter=maxiter, initial_values=initial_params,
                            method=method, returninfo=True, algorithm=algo_in,
                            optparams=algo_params,
                            **opt_params
                            )

    return result, initial_params

def Print(results):
    m.print_table(results)