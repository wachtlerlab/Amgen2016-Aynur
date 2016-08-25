import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import rcParams
from BrianUtils.NeuronModels import AdEx
from matplotlib import patches
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


for csvFilename in sys.argv[1:]:
    lst = csvFilename.split(":", 1)
    mode = lst[0]
    csvFilename = lst[1]
    print "Processing", csvFilename
    df = pd.read_csv(csvFilename)
    names = [t for t in df.dtypes.keys() if df.dtypes[t]=="float64"]
    if mode=="":
        print df
    elif mode=="dtype":
        print type(df.dtypes)
        print df.dtypes
    elif mode=="stat":
        print "Calculating stats"
        from scipy.stats import kruskal
        dfstat = pd.DataFrame()
        for i in names:
            print "Parameter", i
            v1 = [k[1][i] for k in df.iterrows() if k[1]["group"] == "young"]
            v2 = [k[1][i] for k in df.iterrows() if k[1]["group"] == "forager"]
            stat, pval = kruskal(v1, v2)
            mean1 = np.mean(v1)
            std1 = np.std(v1)
            mean2 = np.mean(v2)
            std2 = np.std(v2)
            nrow = {"parameter":i, "stat":stat, "pval":pval, "mean_young":mean1, "std_young":std1,
                    "mean_forager": mean2, "std_forager": std2}
            print nrow
            dfstat = dfstat.append(nrow, ignore_index=True)
            fig1, ax1 = plt.subplots(figsize=(8, 12))
            # boxprops = prp1, medianprops = prp1, whiskerprops = prp1
            prp1 = dict(color="r")
            bp = plt.boxplot([v1, v2], positions=[-1., 1.], bootstrap=True, widths=[0.8, 0.8],
                             patch_artist=patches.Patch(), labels=["young", "forager"])
            # prp2 = dict(color="b")
            # ax.boxplot([1], positions=[1.], bootstrap=True, widths=[0.8], patch_artist=patches.Patch())
            ax1.plot([-1.]*len(v1), v1, "ro")
            ax1.plot([1.]*len(v2), v2, "bo")
            plt.title("DIstribution of parameter "+i)
            plt.ylabel(i)
            plt.tight_layout()
            fig1.savefig(csvFilename+".param."+i+".png")
        dfstat.to_csv(csvFilename+".stat")
    elif mode=="float":
        print df.dtypes[df.dtypes=="float64"]
    elif mode=="mean":
        print df.mean()
    elif mode=="regime":
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        color = lambda x: "r" if x=="young" else "b"
        fig, ax = plt.subplots(figsize=(14, 11.2))
        for k, s in df.iterrows():
            f1, f2 = AdEx.ActType(dict(s))
            ax.plot(f1, f2, color=color(s["group"]), marker='o')
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
        # fig.map_upper(plt.scatter)
        # fig.map_lower(plt.scatter)
        # fig.map_diag(sns.kdeplot, legend = True)
        plt.tight_layout()
        plt.show()
