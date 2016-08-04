from NixUtils import ModelfittingIO as mio
from NeoUtils import NeoPlot as PL

def PlotSimulation(exp, location, fname, expsig = True, expspk = True):
    file = mio.ModelfittingIO(exp, location)
    res = file.GetSim(fname)
    spks = []
    sigs = []
    if expsig or expspk:
        sigs, spks = file.GetOut(res["output"])
    sigs += res["monitors"]
    file.closeNixFile()
    PL.PlotSets(sigs, spks)

def PlotOutput(exp, location, out_name, expspk = True):
    file = mio.ModelfittingIO(exp, location)
    sigs, spks = file.GetOut(out_name)
    if not expspk: spks = []
    else: spks = [spks]
    sigs = [sigs]
    file.closeNixFile()
    PL.PlotSets(sigs, spks)

def PlotInput(exp, location, inp_name):
    file = mio.ModelfittingIO(exp, location)
    inp = file.GetIn(inp_name)
    file.closeNixFile()
    PL.PlotSets([inp], [])

def PlotDataArrays(exp, location, inputs, outputs, expspk = True):
    file = mio.ModelfittingIO(exp, location)
    sigs = [file.GetIn(i) for i in inputs]
    outs = [file.GetOut(i) for i in outputs]
    sigs += [n[0] for n in outs]
    spks = [n[1] for n in outs]
    PL.PlotSets(sigs, spks)