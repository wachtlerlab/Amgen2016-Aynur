from Storage import ProjectStructure as ps
import sys

ids = ps.getExpIds()

id = sys.argv[1]
if id=="+":
    di = ps.getSettings()
    ind = ids.index(di["expname"])
    ind = (ind+1)%len(ids)
    di["expname"] = ids[ind]
    ps.setSettings(di)
    print "Set current expname ", ids[ind], " for project ", ps.DATA
elif id=="-":
    di = ps.getSettings()
    ind = ids.index(di["expname"])
    ind = (ind-1)%len(ids)
    di["expname"] = ids[ind]
    ps.setSettings(di)
    print "Set current expname ", ids[ind], " for project ", ps.DATA
elif id in ids:
    di = ps.getSettings()
    di["expname"] = id
    ps.setSettings(di)
    print "Set current expname ", id, " for project ", ps.DATA
else:
    print "Experiment ", id, " doesnt exist in project ", ps.DATA