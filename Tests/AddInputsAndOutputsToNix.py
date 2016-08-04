from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as fs
from NeoUtils import NeoPlot as plt
#"130322-1LY"


for ename in mio.GetAvaliableIds():
    f = mio.ModelfittingIO(ename, fs.FITTING)
    exp = mio.UnpickleExp(ename)

    seg = exp.segments[0]
    aft = exp.segments[1]

    names = plt.GetNames(seg)
    for l in list(set([n for n in names if "Trial" == n[:5]])):
        sig = [k for k in seg.analogsignals if k.name==l]
        spk = [k for k in seg.spiketrains if k.name==l]
        if len(sig)>0 and len(spk)>0: f.AddOut(sig[0], spk[0], name=sig[0].name + "-DuringStimulus")
    l = "PredictedInput1"
    sig = [k for k in seg.analogsignals if k.name==l and k.description=="voltage"]
    if len(sig)>0:
        sig = sig[0]
        sig.name = "subthreshold"
        f.AddIn(sig)
    sig = [k for k in seg.analogsignals if k.name==l and k.description=="current"]
    if len(sig)>0:
        sig = sig[0]
        sig.name = "derivative"
        f.AddIn(sig)

    names = plt.GetNames(aft)
    for l in list(set([n for n in names if "Trial" == n[:5]])):
        sig = [k for k in aft.analogsignals if k.name==l]
        spk = [k for k in aft.spiketrains if k.name==l]
        if len(sig)>0 and len(spk)>0:
            print sig[0].name
            f.AddOut(sig[0], spk[0], name=sig[0].name + "-AfterStimulus")

    f.closeNixFile()