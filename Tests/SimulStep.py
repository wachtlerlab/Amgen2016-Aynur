'''
Was used for simulation and plots of responces of AdEx to a step current.
Usage:
python SimulStep.py regime_name
makes plot for regime regime_name from AdEx model
'''
from BrianUtils.NeuronModels import AdEx
from BrianUtils import Simulator
from NeoUtils import Signals as ss
from NeoUtils import NeoPlot as npl
import quantities as q
import brian as b
import sys

lenS = 400

regime = sys.argv[1]

scaleFactor = float(sys.argv[2]) if len(sys.argv)>2 else 1.

inits = getattr(AdEx.AdEx, regime)

sim = Simulator.Simulator("adex")
sim.set_time(0*b.second)

signal = ss.SignalBuilder(sampling_period=1*q.ms, t_start=0*q.s, length=lenS, units=q.nA).get_rect(0.1*q.s, 0.3*q.s,
                                                                                                   1*q.nA)
signal = signal*(signal.times>100*q.ms)*(signal.times<300*q.ms)
sim.set_input("I", signal)

inits.update({"scaleFactor":scaleFactor, "scaleFactor2":0.})

sigs = sim.run(lenS*b.msecond, 0.01*b.msecond, inits=inits, monitors={"i":b.mA,"V":b.mvolt})

title = "Simulation in regime "+ regime +"."

npl.PlotLists([zip(sigs, [None]*len(sigs))], title=title, legend=False, lw=2)