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
optparams = {"proportion_selective":0.3}

f.FitSomething("adex", input="derivative-DuringAfterStimulus", output="Trial4-DuringAfterSimiulus", maxiter=100,
               inits = inits, optparams=optparams)

lst = f.GetFittingNames()

if len(lst)>0: f.SimulateFitting(lst[-1])