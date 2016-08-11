from NixUtils.NixModelFitter import NixModelFitter
from brian import nA, uA, mV, pF, nS, ms
from BrianUtils.NeuronModels import AdEx

f = NixModelFitter("130322-1LY")

# inits = {
#             "w": 0*uA,
#             "Vr": -70.6 * mV,#-48.5*mV,
#             "Vt":-50.4 * mV,
#             "b": 0.0805 * nA,
#             "V":-70.4 * mV,
#             "sF": 2 * mV,
#             "tau": 144 * ms,
#             "EL": -70.6 * mV,
#             "gL": 30 * nS,
#             "C": 281 * pF,
#             "a": 4 * nS,
#             "Vp": -25 * mV
#         }
inits = AdEx.AdEx.bursting_rebound
# for i in xrange(1, 11, 21, 31, 41, 51)
algoptparams = {"proportion_selective": 0.5}
optparams = ["b", "a", "sF", "Vr", "gL", "C", "Vt", "tau", "scaleFactor"]

f.FitSomething("adex", input="subthreshold-DuringAfterStimulus-e-7", output="Trial4-DuringAfterSimiulus", maxiter=100000,
               inits = inits, algoptparams=algoptparams, from_perc=False)

lst = f.GetFittingNames()

if len(lst)>0: f.SimulateFitting(lst[-1])