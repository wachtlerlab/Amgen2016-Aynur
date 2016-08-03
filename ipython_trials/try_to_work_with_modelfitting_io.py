from nix_utilities import modelfitting_io as mio
from nix_utilities import filesystem as fs
from sig_proc import multiple as mpl
from sig_proc import plot as plt

f = mio.modelfitting_io("130322-1LY", fs.FITTING)
seg = mpl.ReadExperiment("130322-1LY").segments[0]

names = plt.GetNames(seg)

for l in [n for n in names if "Trial" in n]:
    sig = [k for k in seg.analogsignals if k.name==l]
    spk = [k for k in seg.spiketrains if k.name==l]
    if len(sig)>0 and len(spk)>0: f.add_exp_output(sig[0], spk[0])

l = "PredictedInput1"
sig = [k for k in seg.analogsignals if k.name==l and k.description=="voltage"]
if len(sig)>0:
    sig = sig[0]
    sig.name = "subthreshold"
    f.add_input(sig)
sig = [k for k in seg.analogsignals if k.name==l and k.description=="current"]
if len(sig)>0:
    sig = sig[0]
    sig.name = "derivative"
    f.add_input(sig)