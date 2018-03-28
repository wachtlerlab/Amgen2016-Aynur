import NixModelFitter as nix
import sys

f = nix.NixModelFitter(sys.argv[1])

for i in sys.argv[2:]:
    if i=="i": print "All inputs:", f.GetInputNames()
    if i=="o": print "All outputs:", f.GetOutputNames()
    if i=="f": print "All fittings:", f.GetFittingNames()
