from NixUtils.NixModelFitter import NixModelFitter
from BrianUtils.NeuronModels import AdEx
from datetime import datetime

f = NixModelFitter("130523-3LY")

# regimes = ["bursting_rebound", "saddle_integrator", "saddle_resonator", "saddle_resonator2", "saddle_mixed", "hopf_resonator", "hopf_resonator2"]
# regimes = ["saddle_integrator", "hopf_resonator2", "saddle_mixed"]
# regimes = ["saddle_mixed", "saddle_resonator2", "hopf_resonator2"]
regimes = ["bursting_rebound"]


names = []

for i in regimes:

    t = datetime.now()

    inits = getattr(AdEx.AdEx, i)

    iters = 5

    logstr = "Starting time is "+str(t)+"\nInitial point is " + str(i) + "\n" + str(iters) + " iterations\n"

    print i

    algoptparams = {"proportion_selective": 0.5}
    optparams = ["b", "a", "sF", "Vr", "gL", "C", "Vt", "tau", "scaleFactor", "scaleFactor2"]


    res = f.FitSomething("adex", input="subthreshold-DuringAfterStimulus-e-7",
                         output="Trial1-DuringAfterSimiulus", maxiter=iters,
                         inits = inits, algoptparams=algoptparams, from_perc=False,
                         popsize=1000, optparams=optparams, returninfo = True, logstr = logstr)
    names.append(res)

print names