import pandas as pd
import seaborn as sns
from matplotlib import pylab as plt
from matplotlib import rcParams
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
    elif mode=="dt":
        print type(df.dtypes)
        print df.dtypes
    elif mode=="fl":
        print df.dtypes[df.dtypes=="float64"]
    elif mode=="mean":
        print df.mean()
    else:
        sds = mode.split(",")
        numbers = set()
        for j in sds:
            lex = j.split("..")
            if len(lex)==1:
                numbers.add(names[int(lex[0])])
            else:
                s = 0 if lex[0]=="" else int(lex[0])
                e = -1 if lex[1]=="" else int(lex[1])
                numbers.update(set(names[slice(s, e)]))
        print names
        sns.set(style="ticks", color_codes=True)
        fig = sns.pairplot(df, hue="group", palette={"young":"red", "forager":"blue"},
                           vars=list(numbers))
        plt.show()
