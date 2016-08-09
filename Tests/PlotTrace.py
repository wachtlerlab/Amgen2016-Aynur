import  NixUtils.NixModelFitter as NF
import sys

n = -1 if len(sys.argv)<2 else int(sys.argv[1])

f = NF.NixModelFitter("130322-1LY")

inames = f.GetInputNames()
onames = f.GetOutputNames()

if lst: f.PlotSimulation(lst[n], expspk=True, expsig=False)