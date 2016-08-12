from NixUtils.NixModelFitter import NixModelFitter
from brian import nA, uA, mV, pF, nS, ms
from BrianUtils.NeuronModels import AdEx

f = NixModelFitter("130322-1LY")

regimes = ["bursting_rebound", "saddle_integrator", "saddle_resonator", "saddle_mixed", "hopf_resonator"]

names = []

for i in regimes:

    inits = getattr(AdEx.AdEx, i)

    print i

    algoptparams = {"proportion_selective": 0.5}
    optparams = ["b", "a", "sF", "Vr", "gL", "C", "Vt", "tau", "scaleFactor"]

    res = f.FitSomething("adex", input="subthreshold-DuringAfterStimulus-e-7", output="Trial4-DuringAfterSimiulus", maxiter=350,
                   inits = inits, algoptparams=algoptparams, from_perc=False, popsize=1000, optparams=optparams)
    names.append(res)

print names

for k in names:
    f.SimulateFitting(k)