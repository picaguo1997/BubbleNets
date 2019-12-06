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
    BN0_dir = str(BN0_idx) + '.png'
    lines = open(os.path.join(filePath, 'BNLF.txt')).readlines()
    BNLF_idx = int(lines[2][:-1].split('.')[0])
    BNLF_dir = str(BNLF_idx) + '.png'
    return BN0_idx, BN0_dir, BNLF_idx, BNLF_dir



idx = {
    'BN0': -1,
    'BNLF': -1,
    'BN0_dir': "",
    'BNLF_dir': ""
}

cluster = {
    'k_3': {},
    'k_5': {},
    'k_3_centroid': {},
    'k_5_centroid': {}
}

result = {}

subdir = os.listdir(resultDir)
for videoName in subdir:
    if(videoName == '.DS_Store'):
        continue

    #cluster['k_3'], cluster['k_3_centroid'] = cluster(videoName, 3)
    #cluster['k_5'], cluster['k_5_centroid'] = cluster(videoName, 5)
    #cluster_exportPath = os.path.join(exportDir, 'cluster.pk')
    #pickle.dump(cluster, open(cluster_exportPath, 'wb'))

    idx['BN0'], idx['BN0_dir'], idx['BNLF'], idx['BNLF_dir'] = findIdx(videoName)

    print(videoName, idx, cluster)

    result[videoName] = [].append(idx)
    #result[videoName].append(cluster)

pickle.dump(result, open(os.path.join(exportDir, 'default_result.pk'), 'wb'))
