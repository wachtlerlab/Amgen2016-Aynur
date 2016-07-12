import M

def single_cell(Mmodel_object, time=200*M.msecond, initials={'V':-65*M.mvolt, 'I':0*M.mA}, spikes=[], deltaV=3*M.mvolt, monitors=None, prefix="", funcI = None):
    eqs = Mmodel_object.get_model()
    print eqs
    g = M.NeuronGroup(N=1, model = eqs, threshold=None)
    j = M.SpikeGeneratorGroup(1, spiketimes=spikes)
    conn = M.Connection(j, g, "V")
    conn[0,0]=deltaV
    Mmodel_object.set_start_params(g, **initials)
    Mmodel_object.simulate(time, g, d=monitors, funcI=funcI)
    print j.get_spikes(0)
    Mmodel_object.plot_results(prefix=prefix)

