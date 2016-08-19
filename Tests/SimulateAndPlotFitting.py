import  NixUtils.NixModelFitter as NF
import sys

# f = NF.NixModelFitter("130523-3LY", mode="r")
f = NF.NixModelFitter("130523-3LY", mode="r")

lst = f.GetFittingNames()

n = lst[-1] if len(sys.argv)<2 else lst[int(sys.argv[1][1:])] if sys.argv[1][0]=="%" else sys.argv[1]

if len(sys.argv)<2: print lst
else: print n

sigfilter = lambda x: True if x.description=="from the model" and x.name!="w" else False

f.SimulateAndPlotFitting(n, legend = True, sigfilter = sigfilter)