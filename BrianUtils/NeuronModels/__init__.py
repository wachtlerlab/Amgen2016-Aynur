import AdEx, HodgkinHuxley, Izhikevich
from Models import DummyModel, Model

def GetModelById(id):
    AllModels = [AdEx.AdEx, HodgkinHuxley.HodgkinHuxley, Izhikevich.Izhikevich]
    lst = [v for v in AllModels if v.id==id]
    if len(lst)>0: return lst[0]
    else: return None