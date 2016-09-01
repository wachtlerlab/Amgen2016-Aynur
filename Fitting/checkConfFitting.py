
from NixUtils.NixModelFitter import NixModelFitter
from BrianUtils import NeuronModels as nm

def checkConfFitting(task):
    nixMF = NixModelFitter(task["neuron"])
    outputs = nixMF.GetOutputNames()
    inputs = nixMF.GetInputNames()
    modelID = task["model"]
    model = nm.GetModelById(modelID)
    assert not model is None, "No model found with id "+str(modelID)
    regime = getattr(model, task["regime"])
    assert task["input"] in inputs, "There is no input {0} in {1}".format(task["input"], task["neuron"])
    assert not (regime is None), "There is no such regime in {0} model : {1}".format(modelID, task["regeme"])
    assert task["output"] in outputs, "There is no output {0} in {1}".format(task["output"], task["neuron"])
    del nixMF