import os
import cPickle as pickle
from groupimg import *
mainDir = os.getcwd()
exportDir = os.path.join(mainDir, 'Configurations')
resultDir = os.path.join(mainDir, 'data', 'rawData')

def clusterImg(videoName, k):
    checked = True
    while(checked):
        data, centroids = groupimage(videoName, k)
        checked = False
        for key, values in centroids.items():
            if not values:
                checked = True
                break


def findIdx(videoName):
    filePath = os.path.join(resultDir, videoName, 'frame_selection')
    lines = open(os.path.join(filePath, 'BN0.txt')).readlines()
    BN0_idx = int(lines[2][:-1].split('.')[0])
    #BN0_dir = str(BN0_idx) + '.png'
    lines = open(os.path.join(filePath, 'BNLF.txt')).readlines()
    BNLF_idx = int(lines[2][:-1].split('.')[0])
    #BNLF_dir = str(BNLF_idx) + '.png'
    return BN0_idx,  BNLF_idx

cluster = {}
result = {}

writing = False
clustering = True

subdir = os.listdir(resultDir)
if clustering:
    cluster[3] = {}
    cluster[5] = {}
    for videoName in subdir:
        if(videoName == '.DS_Store'):
            continue
        k=3
        loadDir = os.path.join(resultDir, videoName)
        clusterImg(videoName, k)
        dataPath = os.path.join(loadDir, 'cluster_data_' + str(k) + '.pk')
        centPath = os.path.join(loadDir, 'cluster_centroid_' + str(k) + '.pk')
        with open(dataPath, 'r') as f:
            data = pickle.load(f)
        with open(centPath, 'r') as f:
            centroids = pickle.load(f)
        #data = pickle.load(open(os.path.join(loadDir, 'cluster_data_' + str(k) + '.pk'), 'rb'))
        #centroids = pickle.load(open(os.path.join(loadDir, 'cluster_centroid_' + str(k) + '.pk'), 'rb'))
        cluster[k]['data'] = data
        cluster[k]['centroid'] = centroids

        k=5
        clusterImg(videoName, k)
        with open(os.path.join(loadDir, 'cluster_data_' + str(k) + '.pk'), 'r') as f:
            data = pickle.load(f)
        with open(os.path.join(loadDir, 'cluster_centroid_' + str(k) + '.pk'), 'r') as f:
            centroids = pickle.load(f)
        cluster[k]['data'] = data
        cluster[k]['centroid'] = centroids

        result[videoName]= cluster

    print(result)
    pickle.dump(result, open(os.path.join(exportDir, 'clustering.pk'), 'wb'))
else:
    filename = 'clustering.pk'
    result = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    print(result)

if writing:
    for videoName in subdir:
        print(videoName)
        if(videoName == '.DS_Store'):
            continue

        BN0, BNLF = findIdx(videoName)
        result[videoName] = []
        result[videoName].append((BN0, BNLF))

    print(result)

    pickle.dump(result, open(os.path.join(exportDir, 'default_result.pk'), 'wb'))

else:
    filename = 'default_result.pk'
    result = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    print(result)
