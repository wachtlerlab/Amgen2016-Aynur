from NixUtils.NixModelFitter import NixModelFitter
from brian import nA, uA, mV, pF, nS, ms
from BrianUtils.NeuronModels import AdEx

f = NixModelFitter("130322-1LY")

# regimes = ["bursting_rebound", "saddle_integrator", "saddle_resonator", "saddle_resonator2", "saddle_mixed", "hopf_resonator", "hopf_resonator2"]
# regimes = ["saddle_integrator", "hopf_resonator2", "saddle_mixed"]
regimes = ["hopf_resonator2"]


names = []

for i in regimes:

    inits = getattr(AdEx.AdEx, i)

    print i

    algoptparams = {"proportion_selective": 0.5}
    optparams = ["b", "a", "sF", "Vr", "gL", "C", "Vt", "tau", "scaleFactor"]

    res = f.FitSomething("adex", input="subthreshold-DuringAfterStimulus-e-7",
                         output="Trial4-DuringAfterSimiulus", maxiter=50000,
                         inits = inits, algoptparams=algoptparams, from_perc=False,
                         popsize=1000, optparams=optparams, returninfo = False)
    names.append(res)

print names