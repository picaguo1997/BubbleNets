import os
import shutil

# This script copy all images from rootdir to targetdir and match the structure BubbleNets needs
# Make sure DAVIS dataset is under the folder BubbleNets.
mainDir = os.getcwd()
DAVISDir = os.path.join(mainDir, 'DAVIS', 'JPEGImages', '480p')
targetdir = os.path.join(mainDir, 'data', 'rawData')

###############################################################
# WARNING: WILL REMOVE EVERYTHING FROM TARGET DIRECTORY FIRST #
###############################################################
os.system("rm -rf " + targetdir + "*")


subdir = os.listdir(DAVISDir)
for dir in subdir:
    if(dir == '.DS_Store'):
        continue
    addDir = os.path.join(targetdir, dir ,'src')
    if not os.path.exists(addDir):
        os.makedirs(addDir)

for root, dirs, files in os.walk(DAVISDir):
    path_list = root.split(os.sep)
    videoName = path_list[-1]
    for file in files:
        if videoName == "480p":
            continue;
        else:
            imageDir = os.path.join(targetdir, videoName, 'src')
            shutil.copy(os.path.join(DAVISDir, videoName, file), imageDir)
