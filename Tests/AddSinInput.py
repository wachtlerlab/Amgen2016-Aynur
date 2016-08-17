from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as fs
import quantities as q
import NeoUtils as nu
import NeoUtils.Signals as sg
from NeoUtils import NeoPlot as NP

a = sg.SignalBuilder(t_start=0 * q.ms, sampling_period=0.1 * q.ms, length=10000)
sig = a.get_sine(2000 * q.ms, -500 * q.ms, amplitude=1 * q.nA)
sig = sg.ExpandNull(sig, 1500*q.ms)
sig = sg.ShiftSignalNull(sig, 200*q.ms)
NP.PlotLists([[[sig, None]]])

for ename in mio.GetAvaliableIds():
    f = mio.ModelfittingIO(ename, fs.FITTING)
    f.AddIn(sig, name="sine-1-4", description="sinusoide, 1/4 period")
    f.closeNixFile()