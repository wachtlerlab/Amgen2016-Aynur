from ..nix_test import rawDataAnalyse as rd

r = rd.RawDataAnalyser("cont265", "/home/maksutov/NIXFiles/reorg")

print r.getContResps([265])

#print r.nixFile.sections