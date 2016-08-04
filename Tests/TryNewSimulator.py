from NixUtils.NixModelFitter import NixModelFitter


f = NixModelFitter("130322-1LY")

f.FitSomething("adex", input="derivative-6trials", output="6trials-DuringStimulus", maxiter=2)

lst = f.GetFittingNames()

if len(lst)>0: f.SimulateFitting(lst[-1])