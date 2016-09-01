'''
Provides functions and objects to plot neo analogsignals and spiketrains
'''
from astropy.visualization import quantity_support
quantity_support()
from matplotlib import pylab as plt
from neo import AnalogSignal, SpikeTrain
import numpy as np
from matplotlib import rcParams

plParams = {'text.usetex': False,
           'axes.labelsize': 'large',
           'font.size': 24,
           'font.family': 'sans-serif',
           'font.sans-serif': 'computer modern roman',
           'xtick.labelsize': 20,
           'ytick.labelsize': 20,
           'legend.fontsize': 20,
           }
rcParams.update(plParams)

class NeoPlotter(object):
    '''
    Class provides functions to plot neo.AnalogSignals and Spiketrains together
    '''
    def __init__(self):
        '''
        Creates instance
        '''
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
        '''
        Set legend visible or not for a curent subplot
        :param val: bool
        :return: None
        '''
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][2] = val
    def Xlabel(self, xlabel):
        '''
        Set xlabel for a current subplot
        :param xlabel: str
        :return: None
        '''
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][4] = xlabel
    def Ylabel(self, ylabel):
        '''
        Set ylabel for a current subplot
        :param ylabel: str
        :return: None
        '''
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][5] = ylabel
    def Title(self, title):
        '''
        Set title for a current subplot
        :param title:
        :return: None
        '''
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][1] = title
    def PlotSignal(self, signal, colorgroup = None):
        '''
        Add analogsignal to a current subplot
        :param signal: neo.AnalogSignal
        :param colorgroup: int (plots in one colorgroup will have same color. Random color if None)
        :return: None
        '''
        if type(signal)!=AnalogSignal: return False
        if not self.subplots:
            self.Subplot(1, 1, 1, "")
        signal.color = colorgroup
        self.subplots[-1][0].append(signal)
    def PlotSpiketrain(self, spkt, colorgroup = None):
        '''
        Add spiketrain to a current subplot
        :param spkt: neo.SpikeTrain
        :param colorgroup: int (plots in one colorgroup will have same color. Random color if None)
        :return: None
        '''
        if type(spkt)!=SpikeTrain: return False
        spkt.color = colorgroup
        if not self.subplots:
            self.Subplot(1, 1, 1, "")
        self.subplots[-1][1].append(spkt)
    def XRange(self, Xrange):
        '''
        Set range for x-axis in current subplot
        :param Xrange: tuple (float, float)
        :return: None
        '''
        if not self.subplots:
            self.Subplot(1, 1, 1)
        self.subplots[-1][2][6] = Xrange
    def Subplot(self, w, h, n, title = "", legend = True, timeunit = "ms", xlabel = None, ylabel = None, Xrange=None):
        '''
        Add new subplot
        :param w: width of the grid
        :param h: height of the grid
        :param n: position of new subplot in grid (see matplotlib subplot)
        :param title: str, title of subplot
        :param legend: bool
        :param timeunit: str
        :param xlabel: str
        :param ylabel: str
        :param Xrange: tuple (float, float)
        :return: None
        '''
        if xlabel==None: xlabel = "Time, ${0}$".format(timeunit)
        if ylabel==None: ylabel = "Value, Unit"
        self.subplots.append(([], [], [w * 10 + h * 100 + n, title, legend, timeunit, xlabel, ylabel, Xrange]))
    def Show(self, figsize = (16, 12), filename = None, **kwargs):
        '''
        Display all plot contents or save into file
        :param figsize: tuple (float, float) , size of figure
        :param filename: str, where to save (if None, will show() without saving)
        :return: None
        '''
        colors = rcParams['axes.color_cycle']
        fig = plt.figure(figsize=figsize)
        for i in self.subplots:
            ax = fig.add_subplot(i[2][0])
            ax.set_title(i[2][1])
            sp = [np.max((np.abs(x.max()), np.abs(x.min()))) for x in i[0]]
            a = self.GetScale(*sp)
            for j in xrange(len(a)):
                sig = i[0][j]
                nquant = (1.*sig.units/a[j])
                name = str(sig.name ) + "[" + str(nquant) + "]"
                if sig.description: name+=" : " + str(sig.description)
                x = sig.times.rescale(i[2][3])
                y = sig.magnitude * a[j]
                color = str(colors[sig.color]) if not (sig.color is None) else False
                if color: ax.plot(x, y, color, label = name, **kwargs)
                else : ax.plot(x, y, label = name, **kwargs)
            for s in i[1]:
                color = str(colors[s.color]) if not (s.color is None) else None
                if color == None: color = np.random.rand(3, 1)
                for m in s.times:
                    x = m.rescale(i[2][3])
                    ax.axvline(x, linestyle="--", color=color)
            if i[2][2]: ax.legend()
            ax.set_xlabel(i[2][4])
            ax.set_ylabel(i[2][5])
            if not i[2][6] is None: ax.set_xlim(i[2][6])
        #plt.tight_layout()
        if filename is None:
            plt.show()
        else:
            fig.savefig(filename)


def PlotLists(lst, title = "", legend = True, sigfilter = lambda x:True, spkfilter = lambda x:True,
              savesize = None, savename = None, **kwargs):
    '''
    Plots analogsignals and corresponding spiketrains using NixPlotter on a single subplot
    :param lst: [(neo.AnalogSignal, neo.Spiketrain), ...]
    :param title: str
    :param legend: bool
    :param sigfilter: function(neo.AnalogSignal):bool - decides, which signal to plot, and which not
    :param spkfilter: function(neo.SpikeTrain):bool - decides, which spiketrain to plot and which not
    :param savesize: size of figure to save. If None, would show on screen without saving
    :param savename: filename, where to save plot
    :return:
    '''
    print "SAVESIZE = ", savesize
    f = NeoPlotter()
    for i in xrange(len(lst)):
        f.Subplot(1, len(lst), i+1, title=title, legend = legend)
        cl = 0
        for k in lst[i]:
            if sigfilter(k[0]):
                f.PlotSignal(k[0], colorgroup=cl)
            if spkfilter(k[1]):
                f.PlotSpiketrain(k[1], colorgroup=cl)
            cl+=1
    f.Show(figsize=savesize, filename=savename, **kwargs)