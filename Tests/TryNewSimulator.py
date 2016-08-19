from NixUtils.NixModelFitter import NixModelFitter
from brian import nA, uA, mV, pF, nS, ms
from BrianUtils.NeuronModels import AdEx

f = NixModelFitter("130322-1LY")

inits = AdEx.AdEx.bursting_rebound

algoptparams = {"proportion_selective": 0.5}
optparams = ["b", "a", "sF", "Vr", "gL", "C", "Vt", "tau", "scaleFactor"]

f.FitModel("adex", input="subthreshold-DuringAfterStimulus-e-7", output="Trial4-DuringAfterSimiulus", maxiter=5,
           inits = inits, algoptparams=algoptparams, from_perc=False, popsize=10000)

lst = f.GetFittingNames()

if len(lst)>0: f.SimulateFitting(lst[-1])