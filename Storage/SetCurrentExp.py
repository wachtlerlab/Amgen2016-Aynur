from Storage import ProjectStructure as ps
import sys

ids = ps.getExpIds()

id = sys.argv[1]

if id in ids:
    di = ps.getSettings()
    di["expname"] = id
    ps.setSettings(di)
    print "Set current expname ", id, " for project ", ps.DATA
else:
    print "Experiment ", id, " doesnt exist in project ", ps.DATA