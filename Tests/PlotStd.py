import  NixUtils.NixModelFitter as NF
import sys

n = -1 if len(sys.argv)<2 else int(sys.argv[1])

f = NF.NixModelFitter("130322-1LY", dir = "/home/maksutov/Public/atlas/DATA/FITTING/backup_12Aug")

lst = f.GetFittingNames()

print lst[n]

if lst: f.PlotStd(lst[n])