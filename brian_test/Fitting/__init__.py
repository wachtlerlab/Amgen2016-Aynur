from brian.library import modelfitting as m
import brian
import quantities as q


import sig_proc as sp


def FitModel(NModel, input, output, popsize=10000, maxiter=100, dt=0.02*brian.ms, method="RK"):

    di = NModel.get_opt_params()
    input_raw = sp.signals.TimedArray_from_AnalogSignal(input)
    output_spk = output.times

    # print "INPUT_RAW:", input_raw.times
    # print "OUTPUT_RAW:", output_spk

    # sp.multiple.PlotSets([input], [output])

    result = m.modelfitting(NModel.get_model(), NModel.get_reset(), NModel.get_threshold(),
                            data=output_spk, input_var="I", input=input_raw,
                            dt = dt, popsize=popsize,
                            maxiter=maxiter, initial_values=NModel.get_inits(),
                            method=method, returninfo=True, algorithm=m.CMAES,
                            **di
                            )
    return result

def Print(results):
    m.print_table(results)