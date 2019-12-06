import os
import cPickle as pickle
from groupimg import *
mainDir = os.getcwd()
exportDir = os.path.join(mainDir, 'Configurations')
resultDir = os.path.join(mainDir, 'data', 'rawData')

def cluster(videoName, k):
    checked = True
    while(checked):
        groupimage(videoName, k)
        clust_file = os.path.join(os.getcwd(), 'data', 'rawData', videoName, 'cluster_centroid_'+str(k)+'.pk')
        centroids = pickle.load(open(clust_file, 'rb'))
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

cluster = {
    'k_3': {},
    'k_5': {},
    'k_3_centroid': {},
    'k_5_centroid': {}
}

result = {}

writing = False
clustering = False

subdir = os.listdir(resultDir)
if writing:
    for videoName in subdir:
        print(videoName)
        if(videoName == '.DS_Store'):
            continue

        if clustering:
            cluster['k_3'], cluster['k_3_centroid'] = cluster(videoName, 3)
            cluster['k_5'], cluster['k_5_centroid'] = cluster(videoName, 5)

        BN0, BNLF = findIdx(videoName)
        result[videoName] = []
        result[videoName].append((BN0, BNLF))

        if clustering:
            result[videoName]['cluster'] = cluster

    print(result)

    pickle.dump(result, open(os.path.join(exportDir, 'default_result.pk'), 'wb'))

else:
    filename = 'default_result.pk'
    result = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    print(result)
