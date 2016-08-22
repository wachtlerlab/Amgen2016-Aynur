import  NixUtils.NixModelFitter as NF
import sys


# expname = "130313-4Rh"
# expname = "130322-1LY"
# expname = "130326-2Rh"
# expname = "130425-1Al"
# expname = "130501-2Rh"
expname = "130523-3LY"
# expname = "130605-2LY"
# expname = "130705-1LY"
# expname = "140813-2Al"
# expname = "140917-1Al"
# expname = "141030-1Al"

f = NF.NixModelFitter(expname,  mode="r")

lst = f.GetFittingNames()

n = lst[-1] if len(sys.argv)<2 else lst[int(sys.argv[1][1:])] if sys.argv[1][0]=="%" else sys.argv[1]

if len(sys.argv)<2: print lst
else: print n

sigfilter = lambda x: True if x.description=="from the model" and x.name!="w" else False

f.SimulateAndPlotFitting(n, legend = True, sigfilter = sigfilter)