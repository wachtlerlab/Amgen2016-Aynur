from NeoUtils import NeoJsonIO as jio, Signals as ss
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import sys

plParams = {'text.usetex': False,
           'axes.labelsize': 'large',
           'font.size': 24,
           'font.family': 'sans-serif',
           'font.sans-serif': 'computer modern roman',
           'xtick.labelsize': 20,
           'ytick.labelsize': 20,
           'legend.fontsize': 20,
           }
sns.set(rc = plParams)

trlw = 5
splw = 5
sglw = 35

sigpos = 30
simpos = 0
simsc = 0.5
exppos = 0
with sns.axes_style("white"):
    plt.figure(figsize=(40, 30))
    di = jio.LoadJson(sys.argv[1])
    sim = di[0][-2]
    exp = di[0][-1]
    spk = di[1][-1]
    # x = np.linspace(0, float(sim.times[-1].simplified*1000), 1000)
    # y = 2*np.sin(x)*(x<1200)*(x>200)
    # plt.plot(x, y, lw=1, label = "stimulus")
    plt.plot(sim.times.simplified*1000, simsc*sim.magnitude+simpos, lw=trlw, label = "simulation")
    plt.plot(exp.times.simplified*1000, exp.magnitude+exppos, lw=trlw, label = "recording")
    for i in spk.times:
        t = i.simplified.magnitude
        xdsim = np.abs(sim.times.simplified.magnitude - t)
        jsim = xdsim.argmin()
        xdexp = np.abs(exp.times.simplified.magnitude - t)
        jexp = xdsim.argmin()
        ysim, yexp = simsc*sim.magnitude[jsim] + simpos, exp.magnitude[jexp]+exppos
        print jexp, jsim, yexp, ysim
        plt.plot([1000*t, 1000*t], [ysim, yexp], lw = splw, color = "g", linestyle="--")
        # plt.axvline(i.simplified*1000, linestyle="--", color="g", lw=0.5)
    plt.plot([200, 1200], [sigpos, sigpos], lw = sglw, solid_capstyle='butt')
    plt.xlim([100, 1300])
    plt.ylim([sim.magnitude.min()*simsc+simpos-1, sigpos+5])
    plt.axis("off")
    plt.savefig(sys.argv[1]+".nice.png")
    # plt.show()