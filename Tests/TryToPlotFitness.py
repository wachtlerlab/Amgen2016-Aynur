import  NixUtils.NixModelFitter as NF

f = NF.NixModelFitter("130322-1LY")

lst = f.GetFittingNames()

print lst

if lst: f.PlotFitness(lst[-3])