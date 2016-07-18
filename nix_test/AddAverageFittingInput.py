import rawDataAnalyse as rd
import os
dirname = "/home/maksutov/NIXFiles/exp_data"
freqs = [265]
problems = ["121224-1LY"]
sec = []
names = list(set([a[0] for a in map(lambda x:x.split("."), os.listdir(dirname)) if len(a)>1 and a[1]=="h5" and a[0]!="toIgnore"]).difference(set(problems)))
print names
for i in names[:2]:
    try:
        analyser=rd.RawDataAnalyser(i, dirname)
    except:
        print "analyser=rd.RawDataAnalyser(i, dirname)"
    sec.append([i, analyser.getContResps(freqs)])
