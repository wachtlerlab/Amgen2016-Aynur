import os
from Storage import ProjectFileStructure as fs

os.system("scp maksutov@green:~/DATA/config/* "+fs.config)
os.system("scp maksutov@green:~/DATA/OUTPUT/* "+fs.OUTPUT)