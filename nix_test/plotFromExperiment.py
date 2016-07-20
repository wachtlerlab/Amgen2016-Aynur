import rawDataAnalyse as rd
from neoNIXIO import tag2AnalogSignal
import numpy as np
from matplotlib import pylab as plt


class Foo(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.__dict__)
    def __unicode__(self):
        return str(self.__dict__)



def getDataFromExp(exp, aver = 1, model = 1):

    dirname = "/home/maksutov/NIXFiles/reorg/"
    freqs = [265]

    try:
        analyser=rd.RawDataAnalyser(exp, dirname)
    except:
        print "analyser=rd.RawDataAnalyser(i, dirname)"
    sec = [t for t in analyser.getContResps(freqs)[freqs[0]] if len(t)>0]

    spk = analyser.getContSpikes(freqs=freqs, types=None)[freqs[0]]

    myExpSect = analyser.nixFile.sections["VibrationStimulii-Processed"].sections["ContinuousStimulii"
        ].sections["ContinuousStimulusAt265.0"].sections["Fitting1"]
    myFitTag = [t for t in analyser.nixFile.blocks["FittingTraces"].tags if t.metadata == myExpSect]

    res = tag2AnalogSignal(myFitTag[0], 0)

    Ds = "DuringStimulus"
    Bs = "BeforeStimulus"
    As = "AfterStimulus"

    plt.title("During stimulus membrane potential for exp {0} placed in parallel".format(exp))
    xlabel, ylabel = "x", "y"

    i = 0
    DATA = []
    for sc in sec:
        i+=1
        if not Bs in sc or not As in sc or not Ds in sc: continue
        median = np.median(np.concatenate((sc[Bs].magnitude, sc[As].magnitude)))
        xlabel = "Time, $"+str(sc[Ds].times.units)+"$"
        ylabel = "Potential, $"+str(sc[Ds].units)+"$"
        xlong = sc[Ds].times - sc[Ds].times[0]
        step = Foo(str(i))
        step.median = median
        step.shift = sc[Ds].times[0]
        step.xunits = sc[Ds].times.units
        step.yunits = sc[Ds].units
        step.x = xlong[xlong<1.0]
        step.y = (sc[Ds].magnitude-median)[:len(step.x)]
        DATA.append(step)

    if aver:
        Y = np.array([k.y for k in DATA]).mean(axis=0)
        step = Foo("average")
        step.median = np.mean([k.median for k in DATA])
        step.x = DATA[0].x
        step.y = Y
        step.xunits = DATA[0].xunits
        step.yunits = DATA[0].yunits
        DATA.append(step)


    if model:
        x = res.times[res.times<1.0]
        y = res.magnitude[:len(x)]
        step = Foo("fitting")
        step.median = None
        step.x = x
        step.y = y
        step.xunits = DATA[0].xunits
        step.yunits = DATA[0].yunits
        DATA.append(step)

    SPK = []
    i = 0
    for sc in spk:
        i+=1
        if not Bs in sc or not As in sc or not Ds in sc: continue
        step = Foo(str(i))
        step.units = sc[Ds].units
        shift = np.array([x.shift for x in DATA if x.name==step.name])
        dx = 0. if len(shift)==0 else shift[0]
        step.times = np.array(sc[Ds].times)-dx
        SPK.append(step)

    DATAOBJ = Foo("ElectroData")
    DATAOBJ.RAW = DATA
    DATAOBJ.SPIKES = SPK
    DATAOBJ.xlabel = xlabel
    DATAOBJ.ylabel = ylabel
    return DATAOBJ


def plotData(DATA, subplot=True, spikes=True, average = True, fitting = True):
    numsset = range(1, 100)
    plotlist = map(str, numsset)+["average"]*average + ["fitting"]*fitting
    i = 0
    toPlot = [l for l in DATA.RAW if l.name in plotlist]
    val = 100*len(toPlot)+10
    for k in toPlot:
        i+=1
        if subplot: plt.subplot(val+i)
        line = plt.plot(k.x, k.y, label=k.name)
        if spikes:
            for l in [ll for ll in DATA.SPIKES if ll.name==k.name]:
                for x in l.times:
                    plt.axvline(x, linestyle = "--", color = plt.getp(line[0], "color"))
        plt.xlabel(DATA.xlabel)
        plt.ylabel(DATA.ylabel)
        plt.legend()
    plt.show()

