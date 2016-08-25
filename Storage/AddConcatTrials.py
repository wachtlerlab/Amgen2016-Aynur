import NeoUtils.Signals as sg
import quantities as q
from Storage import ProjectFileStructure as fs
from NixUtils import ModelfittingIO as mio

new_neurons = ["130705-1LY", "140813-3Al"]

for ename in [k for k in mio.GetAvaliableIds() if k in new_neurons]:
    f = mio.ModelfittingIO(ename, fs.FITTING)

    inp = f.GetInNames()
    dur = [n for n in f.GetOutNames() if "Trial" == n[:5] and "DuringStimulus" in n]
    aft = [n for n in f.GetOutNames() if "Trial" == n[:5] and "AfterStimulus" in n]

    print "dur:", dur
    print "aft:", aft
    dur.sort()
    aft.sort()
    count = len(dur)
    name = str(count)+"trials"
    iTime = 200*q.ms
    dTime = 1100*q.ms
    duroutputs = [f.GetOut(n) for n in dur]

    print name
    output = sg.ShiftSignalNull(sg.Join_Shifted([n[0] for n in duroutputs], dTime, name=name+"-DuringStimulus"), iTime)
    spks = sg.ShiftSpikeTrain(sg.JoinSpikeTrainsShifted([n[1] for n in duroutputs], dTime), iTime)
    f.AddOut(output, spks, name=output.name)

    inputs = [f.GetIn(n) for n in inp]
    for i in inputs:
        print i.name
        input = sg.ShiftSignalNull(sg.Join_Shifted([i]*count, dTime, name=i.name+"-"+output.name), iTime)
        f.AddIn(input, description="repeated signal")

    aftoutputs = [f.GetOut(n) for n in aft]

    conn = [sg.ConcatSequential(duroutputs[i][0], aftoutputs[i][0], name=dur[i][:-14]+"DuringAfterSimiulus",
                                description="Trace") for i in xrange(count)]

    conn_spk = [sg.JoinSpikeTrains([duroutputs[i][1], sg.ShiftSpikeTrain(aftoutputs[i][1],
                                                                         duroutputs[i][0].t_start +
                                                                         duroutputs[i][0].duration)])
                for i in xrange(count)]

    for i in xrange(count):
        f.AddOut(sg.ShiftSignalNull(conn[i], iTime), sg.ShiftSpikeTrain(conn_spk[i], iTime))
        f.AddOut(conn[i], conn_spk[i], name=conn[i].name+"-unshifted")


    iTime = 200*q.ms
    dTime = 1600*q.ms

    sig = sg.ShiftSignalNull(sg.Join_Shifted(conn, dTime, name = name+"-DuringAfterStimulus"), iTime)
    spk = sg.ShiftSpikeTrain(sg.JoinSpikeTrainsShifted(conn_spk, dTime), iTime)
    f.AddOut(sig, spk, name = sig.name)

#    sDur = 1520*q.ms

    for i in inputs:
        input = sg.ShiftSignalNull(sg.Join_Shifted([i]*count, dTime, name=i.name+"-"+sig.name), iTime)
        f.AddIn(input, description="repeated signal")
        input = sg.ShiftSignalNull(sg.ExpandNull(i, conn[0].duration), iTime)
        input.name = input.name+"-DuringAfterStimulus"
        f.AddIn(input, description="expanded input")


    f.closeNixFile()