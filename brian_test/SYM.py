from M import ms, mV, mA, uA
import M

def single_cell(Nmodel, time=200*ms, inits={'V': -65 * mV, 'I': 0 * mA}, spikes=[], dV=3*mV, monitors=None, prefix=""):
    eqs = Nmodel.get_model()
    print eqs
    print "T,R = ", Nmodel.get_threshold(), Nmodel.get_reset()
    if Nmodel.get_threshold()!=None:
        g = M.NeuronGroup(N=1, model = eqs, threshold=Nmodel.get_threshold(), reset=Nmodel.get_reset())
    else: g = M.NeuronGroup(N=1, model = eqs, threshold=None)
    j = M.SpikeGeneratorGroup(1, spiketimes=spikes)
    conn = M.Connection(j, g, "V")
    conn[0,0]=dV
    Nmodel.set_start_params(g, **inits)
    Nmodel.simulate(time, g, d=monitors)
    print j.get_spikes(0)
    Nmodel.plot_results(prefix=prefix)
