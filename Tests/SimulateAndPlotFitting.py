import  NixUtils.NixModelFitter as NF
import sys

f = NF.NixModelFitter("130322-1LY", mode="r")

lst = f.GetFittingNames()

n = lst[-1] if len(sys.argv)<2 else lst[int(sys.argv[1][1:])] if sys.argv[1][0]=="%" else sys.argv[1]

if len(sys.argv)<2: print lst
else: print n

f.SimulateAndPlotFitting(n, legend = True)