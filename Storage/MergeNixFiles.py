'''
Not more necessary. Don't Use!
'''
import datetime as dt
import os
import sys

import NixUtils.ModelfittingIO as mio
from Storage import ProjectStructure as FS

tempFolder = "/tmp/nixfiles"

dbool = True
greenFolder = "/home/maksutov/DATA/FITTING/"
if len(sys.argv)>1:
    if sys.argv[1][0]=="!":
        dbool = False
    elif sys.argv[1][0]!=":":
        greenFolder = sys.argv[1]


time = str(dt.datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")



mergedFolder = os.path.join(FS.FITTING, "merged" + str(time))
os.mkdir(mergedFolder)

if dbool:
    if os.path.exists(tempFolder): os.system("rm -r "+tempFolder)
    os.mkdir(tempFolder)
    os.system("scp maksutov@green:" + greenFolder + "*.h5 " + tempFolder)

saphlist = [k for k in os.listdir(FS.FITTING) if ".h5" in k]
atlasFList = [x for x in os.listdir(FS.FITTING) if ".h5" in x]
tempFList = os.listdir(tempFolder)
excl = [x for x in atlasFList if not x in tempFList]

for i in excl:
    print "Copying from atlas: ", i
    atlasNixName = os.path.join(mergedFolder, i)
    atlasOldNixName = os.path.join(FS.FITTING, i)
    os.system("cp {0} {1}".format(atlasOldNixName, atlasNixName))

for i in tempFList:
    if ".h5" in i:
        greenNixName = os.path.join(tempFolder, i)
        atlasNixName = os.path.join(mergedFolder, i)
        atlasOldNixName = os.path.join(FS.FITTING, i)
        if os.path.exists(atlasOldNixName):
            print "Merging ", i
            os.system("cp {0} {1}".format(atlasOldNixName, atlasNixName))
            atlasNixFile = mio.ModelfittingIO(i.split(".")[0], mergedFolder)
            greenNixFile = mio.ModelfittingIO(i.split(".")[0], tempFolder)
            greenFittings = greenNixFile.GetFitNames()
            atlasFittings = atlasNixFile.GetFitNames()
            for fittingName in greenFittings:
                if not fittingName in atlasFittings:
                    fittingFromGreen = greenNixFile.GetFit(fittingName)
                    atlasNixFile.AddFit(fittingName, fittingFromGreen["model"], None, initials=fittingFromGreen["inits"],
                                        best_pos=fittingFromGreen["fitted"], in_name = fittingFromGreen["input"],
                                        out_name = fittingFromGreen["output"], input_var=fittingFromGreen["input_var"],
                                        description="green")
            greenNixFile.closeNixFile()
            atlasNixFile.closeNixFile()
        else:
            print "Copying from green: ", i
            os.system("cp {0} {1}".format(greenNixName, atlasNixName))