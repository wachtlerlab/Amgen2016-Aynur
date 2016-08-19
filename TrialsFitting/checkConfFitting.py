from NixUtils.NixModelFitter import NixModelFitter
from BrianUtils.NeuronModels import AdEx

def checkConfFitting(task):
    nixMF = NixModelFitter(task["neuron"])
    outputs = nixMF.file.GetOutNames()
    inputs = nixMF.file.GetInNames()
    model = task["model"]
    regime = getattr(AdEx.AdEx, task["regime"])
    assert model=="adex", "Model id is not adex"
    assert task["input"] in inputs, "There is no input {0} in {1}".format(task["input"], task["neuron"])
    assert not (regime is None), "There is no such regime in adex model : "+task["regeme"]
    assert task["output"] in outputs, "There is no output {0} in {1}".format(task["output"], task["neuron"])