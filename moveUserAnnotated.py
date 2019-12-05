import os
import shutil

rootdir = '/Users/rogerlee/Desktop/ECS269/DAVIS/Annotations/480p/'
targetdir = '/Users/rogerlee/Desktop/ECS269/Project/BubbleNets/data/rawData/'


def findFile(subdir): # locate which annotated image to be copied
    file= targetdir + subdir + '/frame_selection/BN0.txt'
    lines = open(file).readlines()
    targetFileName = lines[2][:-1].split('.')[0] + '.png'
    return targetFileName


if __name__ == '__main__':

    subdir = os.listdir(rootdir)
    for folder in subdir:
        if(folder == '.DS_Store'):
            continue
        fileName = findFile(folder)
        shutil.copyfile(rootdir + folder + '/' + fileName, targetdir + folder + '/usrAnnotate/' + fileName)