import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import rcParams
from BrianUtils.NeuronModels import AdEx
import numpy as np
import sys

'''plParams = {'text.usetex': False,
           'axes.labelsize': 'large',
           'font.size': 24,
           'font.family': 'sans-serif',
           'font.sans-serif': 'computer modern roman',
           'xtick.labelsize': 20,
           'ytick.labelsize': 20,
           'legend.fontsize': 20,
           }
rcParams.update(plParams)'''


for i in sys.argv[1:]:
    lst = i.split(":", 1)
    mode = lst[0]
    i = lst[1]
    print "Processing", i
    df = pd.read_csv(i)
    names = [t for t in df.dtypes.keys() if df.dtypes[t]=="float64"]
    if mode=="":
        print df
    elif mode=="dtype":
        print type(df.dtypes)
        print df.dtypes
    elif mode=="float":
        print df.dtypes[df.dtypes=="float64"]
    elif mode=="mean":
        print df.mean()
    elif mode=="regeme":
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        young = set(["130523-3LY", "130605-1LY", "130605-2LY", "140813-3Al", "140917-1Al", "140930-1Al", "141030-1Al"])
        color = lambda x: "r" if x in young else "b"
        fig, ax = plt.subplots(figsize=(14, 11.2))
        for k, s in df.iterrows():
            f1, f2 = AdEx.ActType(dict(s))
            ax.plot(f1, f2, color=color(s["neuron"]), marker='o')
            ax.annotate(s['neuron']+", "+s["start"][17:], (f1, f2), size=10)
            print(k, s["neuron"], s["Gamma"], s['start'])
            xmin = min(xmin, f1)
            xmax = max(xmax, f1)
            ymin = min(ymin, f2)
            ymax = max(ymax, f2)
        func1 = lambda x: x
        func2 = lambda x: 0.25 * x * (1 - (1 / x)) ** 2
        x = np.linspace(xmin, xmax, 150)
        y1 = func1(x)
        y2 = func2(x)
        plt.plot(x, y1, "k:", label = "Hopf/Saddle-node")
        plt.plot(x, y2, "k--", label = "Resonator/Integrator")
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
        plt.xlabel("$\\tau_m / \\tau_w$")
        plt.ylabel("$a / g_L$")
        plt.legend()
        plt.show()
    else:
        sds = mode.split(",")
        numbers = set()
        for j in sds:
            lex = j.split("..")
            if len(lex)==1:
                try:
                    numbers.add(names[int(lex[0])])
                except:
                    numbers.add(lex[0])
            else:
                s = 0 if lex[0]=="" else int(lex[0])
                e = -1 if lex[1]=="" else int(lex[1])
                numbers.update(set(names[slice(s, e)]))
        print names
        sns.set(style="ticks", color_codes=True)
        fig = sns.pairplot(df, hue="group", palette={"young":"red", "forager":"blue"},
                           vars=list(numbers), diag_kind="kde")
        plt.tight_layout()
        plt.show()
