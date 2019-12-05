import os
import shutil

# This script copy all images from rootdir to targetdir and match the structure BubbleNets needs

rootdir = '/Users/rogerlee/Desktop/ECS269/DAVIS/JPEGImages/480p/'
targetdir = '/Users/rogerlee/Desktop/ECS269/Project/BubbleNets/data/rawData/'

###############################################################
# WARNING: WILL REMOVE EVERYTHING FROM TARGET DIRECTORY FIRST #
###############################################################
os.system("rm -rf " + targetdir + "*")


subdir = os.listdir(rootdir)
for dir in subdir:
    if(dir == '.DS_Store'):
        continue
    os.system("mkdir " + targetdir + dir + "/")
    os.system("mkdir " + targetdir + dir + "/src")

for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file != '.DS_Store':
                shutil.copyfile(os.path.join(root, file), targetdir + str(root).split('/')[-1] + "/src/" + file)
