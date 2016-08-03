from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as fs
import quantities as q
import NeoUtils as nu
import NeoUtils.Signals as sg


for ename in mio.GetAvaliableIds():
    f = mio.ModelfittingIO(ename, fs.FITTING)

    inp = f.get_input_names()
    out = [n for n in f.get_output_names() if "Trial"==n[:5] and "DuringStimulus" in n]

    count = len(out)
    name = str(count)+"trials"

    iTime = 200*q.ms
    dTime = 100*q.ms

    outputs = [f.get_output(n) for n in out]

    print name
    output = sg.ShiftSignalNull(sg.Join_Shifted([n[0] for n in outputs], dTime, name=name+"-DuringStimulus"), iTime)
    spks = sg.ShiftSpikeTrain(sg.JoinSpikeTrainsShifted([n[1] for n in outputs], dTime), iTime)

    f.add_exp_output(output, spks, name=output.name)

    inputs = [f.get_input(n) for n in inp]
    for i in inputs:
        print i.name
        input = sg.ShiftSignalNull(sg.Join_Shifted([i]*count, dTime, name=i.name+"-"+name), iTime)
        f.add_input(input, description="repeated signal")

    f.close()