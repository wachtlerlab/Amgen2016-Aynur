import os
import socket
import json


'''
Here if you want to use it with your computer, please change HOME to your preferred folder for the project
'''
HOME = os.path.expanduser('~')

if socket.gethostname()=="sapphire": HOME = os.path.join(HOME, "Public", "Trial31")#HOME = os.path.join(HOME, "Public", "atlas")
elif socket.gethostname()=="green": pass

DATA = os.path.join(HOME, "DATA")
INPUT = os.path.join(DATA, "INPUT")
OUTPUT = os.path.join(DATA, "OUTPUT")
FITTING = os.path.join(DATA, "FITTING")
TRACES = os.path.join(DATA, "TRACES")
fpickle = os.path.join(FITTING, "pickle")
temp = os.path.join(DATA, "temp")
analysis = os.path.join(DATA, "analysis")
tables = os.path.join(analysis, "tables")
config = os.path.join(DATA, "config")

expIDs = os.path.join(DATA, "expIDs.json")
settingFile = os.path.join(DATA, "settings.json")

def createExpIdFile(ids_list):
    di = {"ids":ids_list}
    json.dump(di, open(expIDs, "w"))

def getExpIds():
    di = json.load(open(expIDs))
    return di["ids"]

def createFolders():
    if not os.path.exists(DATA):
        os.makedirs(DATA)
    for dr in [OUTPUT, FITTING, TRACES, analysis, tables, config, temp]:
        if not os.path.exists(dr):
            os.makedirs(dr)

def getSettings():
    if not os.path.exists(settingFile):
        di = {"expname":getExpIds()[0]}
        json.dump(di, open(settingFile, "w"))
    return json.load(open(settingFile))

def setSettings(ns):
    json.dump(ns, open(settingFile, "w"))