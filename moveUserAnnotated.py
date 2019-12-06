import os
import shutil

mainDir = os.getcwd()
DAVISDir = os.path.join(mainDir, 'DAVIS', 'Annotations', '480p')
targetdir = os.path.join(mainDir, 'data', 'rawData')
#rootdir = '/Users/rogerlee/Desktop/ECS269/DAVIS/Annotations/480p/'
#targetdir = '/Users/rogerlee/Desktop/ECS269/Project/BubbleNets/data/rawData/'


def findFile(subdir): # locate which annotated image to be copied
    filePath = os.path.join(targetdir, subdir, 'frame_selection', 'BN0.txt')
    file= targetdir + subdir + '/frame_selection/BN0.txt'
    lines = open(filePath).readlines()
    targetFileName = lines[2][:-1].split('.')[0] + '.png'
    return targetFileName


if __name__ == '__main__':

    subdir = os.listdir(DAVISDir)
    for folder in subdir:
        if(folder == '.DS_Store'):
            continue
        fileName = findFile(folder)
        imageDir = os.path.join(targetdir, folder, 'usrAnnotate')
        shutil.copy(os.path.join(DAVISDir, folder, fileName), imageDir)
        #shutil.copyfile(rootdir + folder + '/' + fileName, targetdir + folder + '/usrAnnotate/' + fileName)
