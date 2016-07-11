import rawDataAnalyse  as rd, os
dirname = "/home/maksutov/NIXFiles/exp_data"
nfile = "/home/maksutov/NIXFiles/reorg/cont265.h5"
freqs = [265]
sec = []
for i in os.listdir(dirname):
    if i[-2:]!='h5': continue
    i = i.split(".")[0]
    if i=="toIgnore" or len(i)<3: continue
    analyser=rd.RawDataAnalyser(i, dirname)
    sec.append([i, analyser.getContResps(freqs)])
print sec[0][1][265]

import nix
f = nix.File.open(nfile, nix.FileMode.Overwrite)
cont = f.create_section("continous_stimulii", "stimulii_type")
fs = cont.create_property("frequency", [nix.Value(v) for v in freqs])
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
