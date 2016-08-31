from Storage import ProjectStructure as fs
from NixUtils import ModelfittingIO as mio

new_neurons = ["130705-1LY", "140813-3Al"]

for ename in [k for k in mio.GetAvaliableIds() if k in new_neurons]:
    f = mio.ModelfittingIO(ename, fs.FITTING)
    names = f.GetInNames()
    for i in names:
        if "subthreshold" in i:
            s = f.GetIn(i)
            print s.name, "|", s.description
            f.AddIn(s*1e-7, name=str(s.name)+"-e-7", description=str(s.description)+", scaled by 1e-7")
    f.closeNixFile()