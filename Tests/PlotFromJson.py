from NeoUtils import NeoJsonIO as jio
from NeoUtils import NeoPlot as np
import sys

plt = np.NeoPlotter()

for i in sys.argv[1:]:
    if i[0]=="!":
        f = jio.LoadJson(fname)
        print f
        break
    lst = i.split("%")
    fname = lst[0]
    if len(lst)>1:
        f = jio.LoadJson(fname)
        for k in lst[1:]:
            if k[0]=="T":
                plt.PlotSpiketrain(f[1][int(k[1:])])
            elif k[0]=="A":
                plt.PlotSignal(f[0][int(k[1:])])
            elif k[0]=="S":
                plt.Subplot(int(k[1]), int(k[2]), int(k[3]))
            elif k[0]=="X":
                p = map(float, k[1:].split("_"))
                plt.XRange(p)
            elif k[0]=="L":
                if k[1]=="X":
                    plt.Xlabel(k[2:])
                else: plt.Ylabel(k[2:])
            elif k[0]=="N":
                if k[1]=="F":
                    plt.Legend(False)
                else: plt.Legend(True)
            elif k[0]=="P":
                plt.Show()
    else:
        jio.PlotJsonAnalogSignals(fname)