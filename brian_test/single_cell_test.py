import SYM
initials = {'V' : -65*SYM.M.mvolt, 'I' : 55*SYM.M.mA}
SYM.single_cell(SYM.M.hodjkin_huxley(), 50*SYM.M.msecond, initials)
'''
md = SYM.M.DummyModel()

eqs = md.get_model()#SYM.M.Equations("dV/dt = 1*mV/ms : mV")

print eqs

g = SYM.M.NeuronGroup(N=1, model = eqs, threshold=None)

md.set_start_params(g, **initials)

#p = md.set_monitors(g)
pn = ['V']
pp = {}

def func(pp):
    for i in pn:
        pp[i] = SYM.M.StateMonitor(g, i, record=0)
    print "monitors:", pp
    SYM.M.run(200*SYM.M.msecond)
    return pp

p = func(pp)


print p

for i in p:
    print p[i].times
    SYM.M.plot(p[i].times/SYM.M.ms, p[i][0]/SYM.M.mvolt, label=i)
SYM.M.legend()
SYM.M.show()
'''