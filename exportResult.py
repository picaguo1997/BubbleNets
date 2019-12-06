import os
import cPickle as pickle
from groupimg import *
mainDir = os.getcwd()
exportDir = os.path.join(mainDir, 'Configurations')
resultDir = os.path.join(mainDir, 'data', 'rawData')

def clusterImg(videoName, k):
    checked = True
    while(checked):
        data, centroids, nimages = groupimage(videoName, k)
        checked = False
        for v in range(len(centroids)):
            cent = centroids[v]
            if cent < 0 or cent >= nimages or not cent:
                checked = True
                break
    print(videoName, data, centroids)
    return data, centroids


def findIdx(videoName):
    filePath = os.path.join(resultDir, videoName, 'frame_selection')
    lines = open(os.path.join(filePath, 'BN0.txt')).readlines()
    BN0_idx = int(lines[2][:-1].split('.')[0])
    lines = open(os.path.join(filePath, 'BNLF.txt')).readlines()
    BNLF_idx = int(lines[2][:-1].split('.')[0])
    return BN0_idx,  BNLF_idx

cluster = {}
result_3 = {}
result_5 = {}

writing = False
clustering = False

subdir = os.listdir(resultDir)
if clustering:
    result_3 = []
    result_5 = []
    for videoName in subdir:
        if(videoName == '.DS_Store'):
            continue
        cluster_3 = [videoName, [], []]
        cluster_5 = [videoName, [], []]
        k=3
        loadDir = os.path.join(resultDir, videoName)
        data, centroids = clusterImg(videoName, k)
        cluster_3[1] = data
        cluster_3[2] = centroids

        k=5
        data, centroids = clusterImg(videoName, k)
        cluster_5[1] = data
        cluster_5[2] = centroids

        result_3.append(cluster_3)
        result_5.append(cluster_5)

    print(result_3)
    pickle.dump(result_3, open(os.path.join(exportDir, 'clustering_3.pk'), 'wb'))
    pickle.dump(result_5, open(os.path.join(exportDir, 'clustering_5.pk'), 'wb'))

else:
    filename = 'clustering_3.pk'
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
    #print(result)
