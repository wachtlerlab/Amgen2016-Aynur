from astropy.visualization import quantity_support
quantity_support()
from matplotlib import pylab as plt
from Signals import CutFirst
from neo import AnalogSignal, SpikeTrain
import numpy as np
import quantities as q
from matplotlib import rcParams


class NeoPlotter(object):
    def __init__(self):
        self.subplots = []
    def GetScale(self, *arr):
        x = np.abs(np.array(arr))
        m = np.median(x)
        p = np.ones(len(x))
        sq, sq2 = np.sqrt(10), np.sqrt(2)
        msq, msq2 = m*sq, m*sq2
        dsq, dsq2 = m/sq, m/sq2
        for i in xrange(len(x)):
            while x[i] < dsq:
                x[i] *= 10
                p[i] *= 10
            while x[i] > msq:
                x[i] /= 10
                p[i] /= 10
            if x[i] > msq2:
                x[i] /= 2
                p[i] /= 2
            elif x[i] < dsq2:
                x[i] *= 2
                p[i] *= 2
        return p
    def Legend(self, val = True):
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][2] = val
    def Xlabel(self, xlabel):
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][4] = xlabel
    def Ylabel(self, ylabel):
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][5] = ylabel
    def Title(self, title):
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][1] = title
    def PlotSignal(self, signal, colorgroup = None):
        if type(signal)!=AnalogSignal: return False
        if not self.subplots:
            self.Subplot(1, 1, 1, "")
        signal.color = colorgroup
        self.subplots[-1][0].append(signal)
    def PlotSpiketrain(self, spkt, colorgroup = None):
        if type(spkt)!=SpikeTrain: return False
        spkt.color = colorgroup
        if not self.subplots:
            self.Subplot(1, 1, 1, "")
        self.subplots[-1][1].append(spkt)
    def Subplot(self, w, h, n, title = "", legend = True, timeunit = "ms", xlabel = None, ylabel = None):
        if xlabel==None: xlabel = "Time, ${0}$".format(timeunit)
        if ylabel==None: ylabel = "Value, Unit"
        self.subplots.append(([], [], [w * 10 + h * 100 + n, title, legend, timeunit, xlabel, ylabel]))
    def Show(self):
        colors = rcParams['axes.color_cycle']
        for i in self.subplots:
            plt.subplot(i[2][0])
            plt.title(i[2][1])
            sp = [np.max((np.abs(x.max()), np.abs(x.min()))) for x in i[0]]
            a = self.GetScale(*sp)
            for j in xrange(len(a)):
                sig = i[0][j]
                nquant = (1.*sig.units/a[j])
                name = str(sig.name) + "[" + str(nquant) + "]"
                if sig.description: name+=" : " + str(sig.description)
                x = sig.times.rescale(i[2][3])
                y = sig.magnitude * a[j]
                color = str(colors[sig.color]) if not (sig.color is None) else False
                if color: plt.plot(x, y, color, label = name)
                else : plt.plot(x, y, label = name)
            for s in i[1]:
                color = str(colors[s.color]) if not (s.color is None) else None
                _plot_single_spike_train(s, timeunit=i[2][3], color = color)
            if i[2][2]: plt.legend()
            plt.xlabel(i[2][4])
            plt.ylabel(i[2][5])
        plt.show()

def PlotLists(lst, title = "", legend = True):
    f = NeoPlotter()
    for i in xrange(len(lst)):
        f.Subplot(1, len(lst), i+1, title=title, legend = legend)
        cl = 0
        for k in lst[i]:
            f.PlotSignal(k[0], colorgroup=cl)
            f.PlotSpiketrain(k[1], colorgroup=cl)
            cl+=1
    f.Show()


def _plot_single_spike_train(spk, color = None, timeunit=q.ms, linestyle="--"):
    if color==None: color = np.random.rand(3, 1)
    for m in spk.times:
        x = m.rescale(timeunit)
        plt.axvline(x, linestyle="--", color = color)

def _plot_single_analog_signal(signal, color=None, plotlabel = False, timeunit = q.ms, valunit = None):
    if valunit==None: valunit = signal.units
    dims = ", ["+str(valunit.dimensionality)+"]"
    label = str(signal.description)+dims if plotlabel else str(signal.name)+", "+str(signal.description)+dims
    x = signal.times.rescale(timeunit)
    y = signal.rescale(valunit)
    l = plt.plot(x, y, label=label, color=color)
    color = plt.getp(l[0], "color")
    plt.legend()
    return color

def plot_single_analog_signal(signal):
    plt.xlabel(CutFirst(signal.times.units))
    plt.ylabel(CutFirst(signal.units))
    _plot_single_analog_signal(signal)
    plt.show()



def plot_block(blk, subplots = True, func = None):
    for seg in blk.segments:
        _plot_segment(seg, subplots=subplots, func = func)
    plt.show()

def show():
    plt.show()

def subplot(w, h, n):
    return plt.subplot(w*10+h*100+n)

def GetNames(seg):
    names = set()
    for i in seg.spiketrains:
        names.add(i.name)
    for i in seg.analogsignals:
        names.add(i.name)
    return sorted(names)

def _plot_segment(seg, subplots=False, func = None):
    names = GetNames(seg)
    if func!=None:
        names = [n for n in names if func(n)]
    plt.title(seg.name)
    l = len(names)
    num = 0
    for i in names:
        num+=1
        if subplots:
            ax = subplot(1, l, num)
            ax.set_title(i, y = 0.8)
            ax.set_xlabel("time, ms")
            ax.set_ylabel("value, unit")
        ans = [k for k in seg.analogsignals if k.name==i]
        spk = [k for k in seg.spiketrains if k.name==i]
        color = None
        for j in ans:
            color = _plot_single_analog_signal(j, color, plotlabel=subplots)
            if (subplots): color=None
        for j in spk:
            _plot_single_spike_train(j, color)
        if not subplots:
            plt.xlabel = "time, ms"
            plt.ylabel = "value, unit"
    plt.legend()

def plot_segment(seg, timeunit=q.ms, func = None):
    _plot_segment(seg, timeunit, func=func)
    show()

def PlotExperiment(block, subplots=True, func = lambda x:True):
    plot_block(block, subplots, func)

def PlotSets(sigs=[], spks=[], timeunit=q.ms, spikelines="--", title = ""):
    if sigs!=None:
        for s in sigs:
            _plot_single_analog_signal(s, timeunit=timeunit)
    if spks!=None:
        for s in spks:
            _plot_single_spike_train(s, timeunit=timeunit, linestyle=spikelines)
    plt.xlabel("Time, "+str(timeunit))
    plt.ylabel("Value, unit")
    plt.legend(loc=2)
    plt.grid(True)
    plt.title(title)
    show()