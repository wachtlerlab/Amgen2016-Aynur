'''
Usages:

python SimulateAndPlotFitting.py -1
will simulate and plot last fitting in current neuron

python SimulateAndPlotFitting.py %fitting_name
will simulate and plot fitting with name fitting_name
'''
import  NixUtils.NixModelFitter as NF
from Storage import ProjectStructure as ps
import sys



expname = ps.getSettings()["expname"]

f = NF.NixModelFitter(expname,  mode="r")

lst = f.GetFittingNames()

n = lst[-1] if len(sys.argv)<2 else sys.argv[1][1:] if sys.argv[1][0]=="%" else lst[int(sys.argv[1])]

if len(sys.argv)<2: print lst
else: print n

sigfilter = lambda x: True if x.description=="from the model" and x.name!="w" else False

f.SimulateAndPlotFitting(n, legend = True, sigfilter = sigfilter)