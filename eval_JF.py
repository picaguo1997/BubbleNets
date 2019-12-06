import os
import sys;
cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, 'generate_labels'));
from seg_eval import *
"""
Important things:
1. Check f_boundary.py and jaccard.py are under this same folder
    If not, go to generate_labels/davis_python/lib/davis/measures
    Copy and paste f_boundary.py and jaccard.py under this same folder
2. And then pip install joblib

Then everything should be fine.
"""
mainDir = os.getcwd()
#help yourself to change the directory:)
videoName = 'scooter-black'
UserDir = os.path.join(mainDir, 'results','OSVOS', videoName)
GTDir = os.path.join(mainDir, 'results', 'GroundTruth', videoName)
J, F = segmentation_score(UserDir,GTDir)
print(J,F)
