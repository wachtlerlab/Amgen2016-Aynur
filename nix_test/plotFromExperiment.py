import rawDataAnalyse as rd
from neoNIXIO import tag2AnalogSignal, sliceAnalogSignal
import numpy as np
from matplotlib import pylab as plt
import neo
import pprint

dirname = "/home/maksutov/NIXFiles/reorg/"
freqs = [265]

exp ="" #"= raw_input("Enter exp.name (default '130605-2LY')")
if exp=="":
    exp = '130605-2LY'
try:
    analyser=rd.RawDataAnalyser(exp, dirname)
except:
    print "analyser=rd.RawDataAnalyser(i, dirname)"
sec = [t for t in analyser.getContResps(freqs)[freqs[0]] if len(t)>0]


myExpSect = analyser.nixFile.sections["VibrationStimulii-Processed"].sections["ContinuousStimulii"
    ].sections["ContinuousStimulusAt265.0"].sections["Fitting1"]
myFitTag = [t for t in analyser.nixFile.blocks["FittingTraces"].tags if t.metadata == myExpSect]

res = tag2AnalogSignal(myFitTag[0], 0)

Ds = "DuringStimulus"
Bs = "BeforeStimulus"
As = "AfterStimulus"


plt.title("During stimulus membrane potential for exp {0} placed in parallel".format(exp))

aver = 1
model = 1
count = len(sec)
val = (count+aver+model)*100+10
i = 0
DATA = []
xlabel, ylabel = "x", "y"

for sc in sec:
    i+=1
    if not Bs in sc or not As in sc or not Ds in sc: continue
    median = np.median(np.concatenate((sc[Bs].magnitude, sc[As].magnitude)))
    xlabel = "Time, $"+str(sc[Ds].times.units)+"$"
    ylabel = "Potential, $"+str(sc[Ds].units)+"$"
    x = sc[Ds].times - sc[Ds].times[0]
    x = x[x<1.0]
    y = (sc[Ds].magnitude-median)[:len(x)]
    DATA.append({"x":x, "y":y, "xunits":sc[Ds].times.units, "yunits":sc[Ds].units,
                 "name":str(i),
                 "median":median,
                 "place":val+i
                 })


if aver:
    Y = np.array([k["y"] for k in DATA]).mean(axis=0)
    DATA.append({"x":DATA[0]["x"], "y":Y, "name":"average",
                "median":np.mean([k["median"] for k in DATA]),
                "place":val+count+1})

if model:
    x = res.times[res.times<1.0]
    y = res.magnitude[:len(x)]
    DATA.append({"x":x, "y":y, "name":"fitting",
                "median":None,
                "place":val+count+2})
numsset = range(1, 100)
plotset = set(map(str, numsset)+["average","fitting"])
for k in [k for k in DATA if k["name"] in plotset]:
    plt.subplot(k["place"])
    plt.plot(k["x"], k["y"], label=k["name"])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
plt.show()