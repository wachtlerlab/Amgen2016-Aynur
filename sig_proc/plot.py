from astropy.visualization import quantity_support
quantity_support()
from matplotlib import pylab as plt
import quantities as q


def __plot_single_analog_signal(signal, color=None, plotlabel = False, timeunit = q.ms, valunit = None):
    if valunit==None: valunit = signal.units
    dims = ", ["+str(valunit)+"]"
    label = str(signal.description)+dims if plotlabel else str(signal.name)+", "+str(signal.description)+dims
    x = signal.times.rescale(timeunit)
    y = signal.rescale(valunit)
    l = plt.plot(x, y, label=label, color=color)
    color = plt.getp(l[0], "color")
    plt.legend()
    return color


def plot_single_analog_signal(signal):
    plt.xlabel(signal.times.units)
    plt.ylabel(signal.units)
    __plot_single_analog_signal(signal)
    plt.show()

def __plot_single_spike_train(spk, col = None, timeunit=q.ms):
    for m in spk.times:
        x = m.rescale(timeunit)
        plt.axvline(x, linestyle="--", color = col)

def plot_block(blk, subplots = True, func = None):
    for seg in blk.segments:
        __plot_segment(seg, subplots=subplots, func = func)
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


def __plot_segment(seg, subplots=False, func = None):
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
            color = __plot_single_analog_signal(j, color, plotlabel=subplots)
            if (subplots): color=None
        for j in spk:
            __plot_single_spike_train(j, color)
        if not subplots:
            plt.xlabel = "time, ms"
            plt.ylabel = "value, unit"
    plt.legend()

def plot_segment(seg, timeunit=q.ms, func = None):
    __plot_segment(seg, timeunit, func=func)
    show()