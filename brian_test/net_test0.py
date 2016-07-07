import brian as B
eqs='''dV/dt = -(V-El)/tau : mvolt'''
Vt = -50*B.mvolt
Vr = -60*B.mvolt
El = -49 *B.mvolt
psp = 0.9*B.mvolt
tau = 20*B.msecond
group = B.NeuronGroup(N=30, model=eqs, threshold=Vt, reset = Vr)
group.V = Vr + B.rand(30)*(Vt-Vr)
conn = B.Connection(group, group)
conn.connect_random(sparseness=0.1 , weight=psp)
monitor = B.SpikeMonitor(group)
state =  B.StateMonitor(group, 'V', record=True)
B.run(0.2*B.second)
print type(state)
for i in state:
    B.plot(state.times/B.ms, i/B.mV)
B.xlabel('Time, ms')
B.ylabel('Membrane potential, mV')
B.title('Membrane potential recroding')
B.show()