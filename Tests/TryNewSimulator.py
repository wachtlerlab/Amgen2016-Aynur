from NixUtils.NixModelFitter import NixModelFitter


f = NixModelFitter("130322-1LY")


# for i in xrange(1, 11, 21, 31, 41, 51)
f.FitSomething("adex", input="derivative-DuringAfterStimulus", output="Trial4-DuringAfterSimiulus", maxiter=10)

lst = f.GetFittingNames()

if len(lst)>0: f.SimulateFitting(lst[-1])