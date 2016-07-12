import M

def single_cell(Mmodel_object, time=200*M.msecond, initials = {'V':-65*M.mvolt, 'I':0*M.mA}):
    eqs = Mmodel_object.get_model()
    print eqs
    g = M.NeuronGroup(N=1, model = eqs, threshold=None)
    Mmodel_object.set_start_params(g, **initials)
    Mmodel_object.simulate(time, g)
    Mmodel_object.plot_results()

