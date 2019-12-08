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

def compare(cluster_sug, default_sug, vid_cluster):
    for k in vid_cluster:
        if cluster_sug in k and default_sug in k:
            return True
    print(cluster_sug, default_sug, vid_cluster)
    return False

cluster = {}
result_3 = {}
result_5 = {}

writing = False
clustering = False
comparing = True

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
    #print(result)

if writing:
    for videoName in subdir:
        print(videoName)
        if(videoName == '.DS_Store'):
            continue

        BN0, BNLF = findIdx(videoName)
        result[videoName] = []
        result[videoName].append((BN0, BNLF))

    print(result)

    pickle.dump(result, open(os.path.join(exportDir, 'clust_3_result.pk'), 'wb'))

else:
    filename = 'clust_3_result.pk'
    result = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    #print(result)
    filename = 'default_result.pk'
    default_result = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    #print(default_result)

if comparing:
    comparison_result = []
    filename = 'clustering_3.pk'
    cluster_data = pickle.load(open(os.path.join(exportDir, filename), 'rb'))
    same_clust_counter = 0
    same_sug_counter = 0
    different_but_same = 0
    #print(cluster_data)
    for video in result:
        videoName = video[0]
        cluster_sug = video[1]
        default_sug = default_result[videoName][0][0]
        if(cluster_sug == default_sug):
            same_sug_counter = same_sug_counter + 1
        for vid in range(len(cluster_data)):
            clust = cluster_data[vid]
            if clust[0] == videoName:
                vid_cluster = clust[1]
                #print(videoName, clust)
                break

        same_clust = compare(cluster_sug, default_sug, vid_cluster)

        comp_ans = []

        comp_ans.append(videoName)
        comp_ans.append(cluster_sug)
        comp_ans.append(default_sug)
        comp_ans.append(same_clust)
        if(same_clust):
            same_clust_counter = same_clust_counter + 1
        if same_clust and cluster_sug != default_sug:
            different_but_same = different_but_same + 1
        comparison_result.append(comp_ans)

    total_vid = len(comparison_result)
    print("Differene Suggestion but from same cluster ", different_but_same, total_vid)
    print("Same Suggestion ", same_sug_counter, total_vid)
    print("Same suggestion rate: ", float(same_sug_counter) / float(total_vid))
    print("Same Clustering " ,same_clust_counter, total_vid)
    print("Same cluster rate: ", float(same_clust_counter) / float(total_vid))
    print(comparison_result)
    filename = 'comparison_result.pk'
    comp_result = pickle.dump(comparison_result, open(os.path.join(exportDir, filename), 'wb'))
