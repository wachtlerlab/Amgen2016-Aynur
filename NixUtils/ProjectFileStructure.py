import os
import socket

HOME = os.path.expanduser('~')
if socket.gethostname()=="sapphire": HOME = os.path.join(HOME, "Public", "atlas")

DATA = os.path.join(HOME, "DATA")
reorg = os.path.join(DATA, "reorg")
INPUT = os.path.join(DATA, "INPUT")
OUTPUT = os.path.join(DATA, "OUTPUT")
FITTING = os.path.join(DATA, "FITTING")
TRACES = os.path.join(DATA, "TRACES")
fpickle = os.path.join(FITTING, "pickle")
nxpickle = os.path.join(reorg, "pickle")


def nixName(exp):
    return str(exp)+".h5"

def getInput(exp, fname=False):
    path = os.path.join(INPUT, exp)
    if not os.path.exists(path):
        os.makedirs(path)
    if fname:
        path = os.path.join(path, fname)
    return path

def getOutput(exp, fname=False):
    path = os.path.join(OUTPUT, exp)
    if not os.path.exists(path):
        os.makedirs(path)
    if fname:
        path = os.path.join(path, fname)
    return path

def getFitting(exp, fname=False):
    path = os.path.join(FITTING, exp)
    if not os.path.exists(path):
        os.makedirs(path)
    if fname:
        path = os.path.join(path, fname)
    return path

def getTraces(exp, fname=False):
    path = os.path.join(TRACES, exp)
    if not os.path.exists(path):
        os.makedirs(path)
    if fname:
        path = os.path.join(path, fname)
    return path

def getReorgFile(exp):
    path = os.path.join(reorg, nixName(exp))
    if not os.path.exists(path):
        raise Exception("Experiment {0} doesn't exist in directory {1}".format(exp, reorg))
    return path