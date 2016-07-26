from brian_test.NeuronModels import Models
from brian_test.NeuronModels.Models import ms, mV


def single_cell(Nmodel, time=200*ms, inits={}, spikes=[], dV=3*mV, monitors=None, prefix=""):
    eqs = Nmodel.get_model()
    print eqs
    print "Treshold,Reset = ", Nmodel.get_threshold(), Nmodel.get_reset()
    if Nmodel.get_threshold()!=None:
        g = Models.NeuronGroup(N=1, model = eqs, threshold=Nmodel.get_threshold(), reset=Nmodel.get_reset(), method ="RK")
    else: g = Models.NeuronGroup(N=1, model = eqs, threshold=None, method ="RK")
    j = Models.SpikeGeneratorGroup(1, spiketimes=spikes)
    conn = Models.Connection(j, g, "V")
    conn[0,0]=dV
    Nmodel.set_start_params(g, **inits)
    Nmodel.simulate(time, g, d=monitors)
    print j.get_spikes(0)
    Nmodel.plot_results(prefix=prefix)

def single_cell_return(Nmodel, time=200*ms, inits={}, spikes=[], dV=3*mV, monitors=None, prefix=""):
    eqs = Nmodel.get_model()
    print eqs
    print "Treshold,Reset = ", Nmodel.get_threshold(), Nmodel.get_reset()
    if Nmodel.get_threshold()!=None:
        g = Models.NeuronGroup(N=1, model = eqs, threshold=Nmodel.get_threshold(), reset=Nmodel.get_reset(), method ="RK")
    else: g = Models.NeuronGroup(N=1, model = eqs, threshold=None, method ="RK")
    j = Models.SpikeGeneratorGroup(1, spiketimes=spikes)
    conn = Models.Connection(j, g, "V")
    conn[0,0]=dV
    Nmodel.set_start_params(g, **inits)
    Nmodel.simulate(time, g, d=monitors)
    print j.get_spikes(0)
    return Nmodel.return_results()
