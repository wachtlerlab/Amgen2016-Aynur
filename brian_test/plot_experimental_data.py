from nix_utilities import XtractDataFromExp as pe
exp = raw_input("Enter exp.name (default '130605-2LY')")
if exp == "":
    exp = '130605-2LY'
pe.plotData(pe.getDataFromExp(exp), subplot=False, fitting=False, average=False)