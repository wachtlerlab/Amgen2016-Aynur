import brian as B
import json_to_one_lauer as JL

a = JL.fromfile('params.json', '')

eqs = B.Equations('''
    dNa_ch_f/dt = (Na_ch_foo-Na_ch_f)/Na_ch_tf/ms : 1
    dNa_ch_x/dt = (Na_ch_xoo-Na_ch_x)/Na_ch_tx/ms : 1
    Na_ch_cond = Na_ch_max*Na_ch_x**Na_ch_px*Na_ch_f**Na_ch_pf : 1

    Na_ch_current = (Na_rest - V/mV)*Na_ch_cond : 1
    
    dKa_ch_f/dt = (Ka_ch_foo-Ka_ch_f)/Ka_ch_tf/ms : 1
    dKa_ch_x/dt = (Ka_ch_xoo-Ka_ch_x)/Ka_ch_tx/ms : 1
    Ka_ch_cond = Ka_ch_max*Ka_ch_x**Ka_ch_px*Ka_ch_f**Ka_ch_pf : 1

    Ka_ch_current = (Ka_rest - V/mV)*Ka_ch_cond : 1


    dV/dt = (Ka_ch_current + Na_ch_current)*capacity*mV/ms : mV
    ''')
for i in a:
        eqs.substitute(i, str(a[i]))

g = B.NeuronGroup(N=1, model = eqs, threshold=None)

g.V = -60*B.mV

pn = ['V','Na_ch_current', 'Ka_ch_current', 'Na_ch_cond']
p = { i: B.StateMonitor(g, i, record=0) for i in pn}

B.run(200*B.msecond)

for i in p:
    B.plot(p[i].times/B.ms, p[i][0]/B.mV, label=i)

B.legend()
B.show()
'''
KAaI = 0.5
AaI = 0.01*B.mvolt
MAaI = 30*B.mvolt
KAdI = 0.3
AdI = -AaI
MAdI = -MAaI


KBaI = 0.3
BaI = 0.01*B.mvolt
MBaI = -0*B.mvolt
KBdI = 0.1
BdI = -BaI
MBdI = -MBaI

tauI = 1.0*B.msecond

VI = -60.0*B.mvolt

p = {
    'foo':
}

eqs=B.Equations('
    Aa = KAa*(MAa - V) : mV
    Ad = KAd*(MAd - V) : mV
    Ba = KBa*(MBa - V) : mV
    Bd = KBd*(MBd - V) : mV
    a = Aa + Ad : mV
    b = Ba + Bd : mV
    c = a + b : mV
    dV/dt = c/tau : mV
    ', KAa=KAaI, KAd=KAdI, MAa=MAaI, MAd=MAdI,
                KBa=KBaI, KBd=KBdI, MBa=MBaI, MBd=MBdI, tau=tauI)


g.Aa = AaI
g.Ad = AdI
g.Ba = BaI
g.Bd = BdI
g.V = VI

c = B.StateMonitor(g, 'c', record=0)
V = B.StateMonitor(g, 'V', record=0)
Aa = B.StateMonitor(g, 'Aa', record=0)
Ad = B.StateMonitor(g, 'Ad', record=0)
Ba = B.StateMonitor(g, 'Ba', record=0)
Bd = B.StateMonitor(g, 'Bd', record=0)

B.run(200*B.msecond)

B.plot(c.times/B.ms, c[0]/B.mV)
B.plot(Aa.times/B.ms, Aa[0]/B.mV)
B.plot(Ad.times/B.ms, Ad[0]/B.mV)
B.plot(Ba.times/B.ms, Ba[0]/B.mV)
B.plot(Bd.times/B.ms, Bd[0]/B.mV)

B.show()'''