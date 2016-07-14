from ..nix_test import rawDataAnalyse as rd

r = rd.RawDataAnalyser("130326-2Rh.h5", "/home/maksutov/NIXFiles/exp_data")

#print r.getContResps([265])

print r.nixFile.sections