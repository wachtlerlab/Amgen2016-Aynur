import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from BrianUtils.NeuronModels import AdEx
from matplotlib import patches
import numpy as np
import sys




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
        from scipy.stats import kruskal, ttest_ind
        dfstat = pd.DataFrame()
        for i in names:
            print "Parameter", i
            v1 = [k[1][i] for k in df.iterrows() if k[1]["group"] == "young"]
            v2 = [k[1][i] for k in df.iterrows() if k[1]["group"] == "forager"]
            kruskal_stat, kruskal_pval = kruskal(v1, v2)
            t_stat, t_pval = ttest_ind(v1, v2, equal_var=False)
            stat = (np.mean(v1), np.std(v1), np.mean(v2), np.std(v2))
            nrow = {"parameter":i, "kruskal_stat":kruskal_stat, "kruskal_pval":kruskal_pval,
                    "t_stat":t_stat, "t_pval":t_pval,
                    "mean_young":stat[0], "std_young":stat[1],
                    "mean_forager": stat[2], "std_forager": stat[3]}
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
        # xmin = xmax = ymin = ymax = 0
        color = lambda x: "r" if x=="young" else "b"
        xmin = 0.001
        xmax = 10.
        ymin = 0.
        ymax = 10.
        with sns.axes_style("whitegrid"):
            fig, ax = plt.subplots(figsize=(15, 15))
            plParams = {'text.usetex': False,
                        'axes.labelsize': 'large',
                        'font.size': 20,
                        'font.family': 'serif',
                        'font.sans-serif': 'computer modern roman',
                        'xtick.labelsize': 20,
                        'ytick.labelsize': 20,
                        'legend.fontsize': 20,
                    }
            sns.set(rc = plParams)
            func1 = lambda x: x
            func2 = lambda x: 0.25 * x * (1 - (1 / x)) ** 2
            pCount = 450
            logmaxX = np.log10(xmax)
            logminX = np.log10(xmin)
            xlog = np.linspace(logminX, logmaxX, pCount)
            x = np.power(10, xlog)
            pInt = (xlog[-1]-xlog[0])/(pCount+1)/2.
            y1 = func1(x)
            y2 = func2(x)
            plt.semilogx(x, y1, "k:")
            plt.semilogx(x, y2, "k--")
            kwargs = dict(edgecolor=(0,0,0,0), interpolate=True)
            rgbs = np.array([
                (128,205,193),
                (1,133,113),
                (223, 194, 125),
                (166,97,26),
                (245,245,245)
            ])/255.
            arCols = [(xxx[0], xxx[1], xxx[2], 0.5) for xxx in rgbs]
            lup, ldn = [30]*len(x), [0]*len(x)
            limit = np.log10(np.sqrt(0.1))
            c1, c2, c3, c4 = (xlog<=limit+pInt), (xlog<=limit+pInt), (xlog <= 0.+pInt)*(xlog>limit-pInt), xlog>limit-pInt
            ax.fill_between(x, y1, y2, where=c1, facecolor=arCols[0], **kwargs)
            ax.fill_between(x, y1, ldn, where=c2, facecolor=arCols[1], **kwargs)
            ax.fill_between(x, y2, ldn, where=c3, facecolor=arCols[1], **kwargs)
            ax.fill_between(x, y2, lup, where=c2, facecolor=arCols[2], **kwargs)
            ax.fill_between(x, y1, lup, where=c4, facecolor=arCols[2], **kwargs)
            ax.fill_between(x, y1, y2, where=c4, facecolor=arCols[3], **kwargs)
            ax.fill_between(x, y2, ldn, where=x>=1., facecolor=arCols[4], **kwargs)
            ax.text(0.04, 0.5, "Mixed Hopf")
            ax.text(0.1, 3, "Hopf resonator")
            ax.text(0.12, 0.1, "Mixed saddle-node")
            ax.text(0.8, 0.5, "Saddle-node resonator")
            ax.text(3, 0.2, "Saddle-node integrator")
            plty1, plty2, pltf1, pltf2 = [], [], [], []
            for k, s in df.iterrows():
                f1, f2 = AdEx.ActType(dict(s))
                if color(s["group"])=="r":
                    plty1.append(f1)
                    plty2.append(f2)
                else:
                    pltf1.append(f1)
                    pltf2.append(f2)
                print(k, s["neuron"], s["Gamma"], s['start'])
                # xmin, xmax, ymin, ymax = min(xmin, f1), max(xmax, f1), min(ymin, f2), max(ymax, f2)

            ax.scatter(pltf1, pltf2, color="b", marker='x', s=20, linewidths=2, edgecolor="k", label="Forager")
            ax.scatter(plty1, plty2, color="r", marker='x', s=20, linewidths=2, edgecolor="k", label="Young")
                # ax.annotate(s['neuron']+", "+s["start"][17:], (f1, f2), size=10)
            plt.legend()
            plt.xlim([xmin, xmax])
            plt.ylim([ymin, ymax])
            plt.xlabel("$\\tau_m / \\tau_w$")
            plt.ylabel("$a / g_L$")
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
