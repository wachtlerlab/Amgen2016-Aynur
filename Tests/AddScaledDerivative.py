from NixUtils import ModelfittingIO as mio
from NixUtils import ProjectFileStructure as fs

'''for ename in mio.GetAvaliableIds():
    f = mio.ModelfittingIO(ename, fs.FITTING)
    names = f.GetInNames()
    for i in names:
        if "subthreshold" in i:
            s = f.GetIn(i)
            print s.name, "|", s.description
            f.AddIn(s*1e-7, name=str(s.name)+"-e-7", description=str(s.description)+", scaled by 1e-7")
    f.closeNixFile()'''