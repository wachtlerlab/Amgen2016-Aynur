import rawDataAnalyse as rd
import os
dirname = "/home/maksutov/NIXFiles/exp_data"
nfile = "/home/maksutov/NIXFiles/reorg/cont265.h5"
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

'''
#print sec
#import nix
#f = nix.File.open(nfile, nix.FileMode.Overwrite)
cont = f.create_section("ContinuousStimulii", "StimuliiType")
fs = cont.create_property("Frequency", [nix.Value(v) for v in freqs])
for i in sec:
    blk = f.create_block(i[0], "exp_name")
    md = f.create_section(i[0], "raw_metadata")
    blk.metadata = md
    for fr in freqs:
        for j in xrange(len(i[1][fr])):
            k = i[1][fr][j]
            for n in k:
                blk.create_data_array(name=i[0]+"_"+str(fr)+"_"+str(j)+"_"+n, array_type="signal", dtype=k[n].dtype, shape=k[n].shape, data=k[n])
f.close()
'''