from ..nix_test import rawDataAnalyse as rd

r = rd.RawDataAnalyser("141121-1Al", "/home/maksutov/NIXFiles/exp_data")

print r.getContResps([265])

#print r.nixFile.sections