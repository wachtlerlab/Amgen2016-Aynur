from nix_test import plotFromExperiment as pe
import fitSomeModel as fm
exp = ""  # "= raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'

data = pe.getDataFromExp(exp)
pe.plotData(data)