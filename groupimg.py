import os
import shutil
import glob
import math
import argparse
import warnings
import numpy as np
from PIL import Image
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
import cPickle as pickle

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore')

class K_means:

  def __init__(self, k=3, size=False, resample=32):
    self.k = k
    self.cluster = [] # the index of cluster each image belongs to.
    self.cluster_ACTcentroid = [] # each cluster's actual centroid
    self.cluster_IMGcentroid = {} # each cluster's img index closest to actual centroid
    self.cluster_data = {} # image indices that belongs to each cluster. Key is cluster index. Values are image indices.
    self.data = [] # features of each image
    self.end = [] # filenmaes of each image
    self.i = 0
    self.size = size
    self.resample = resample

  def manhattan_distance(self,x1,x2):
    s = 0.0
    for i in range(len(x1)):
      s += abs( float(x1[i]) - float(x2[i]) )
    return s

  def euclidian_distance(self,x1,x2):
    s = 0.0
    for i in range(len(x1)):
      s += math.sqrt((float(x1[i]) - float(x2[i])) ** 2)
    return s

  def read_image(self,im):
    if self.i >= self.k :
      self.i = 0
    try:
      img = Image.open(im)
      osize = img.size
      img.thumbnail((self.resample,self.resample))
      v = [float(p)/float(img.size[0]*img.size[1])*100  for p in np.histogram(np.asarray(img))[0]]
      if self.size :
        v += [osize[0], osize[1]]
      #pbar.update(1)
      i = self.i
      self.i += 1
      return [i, v, im]
    except Exception as e:
      print("Error reading ",im,e)
      return [None, None, None]


  def generate_k_means(self):
    final_mean = []
    for c in range(self.k):
      partial_mean = []
      for i in range(len(self.data[0])):
        s = 0.0
        t = 0
        for j in range(len(self.data)):
          if self.cluster[j] == c :
            s += self.data[j][i]
            t += 1
        if t != 0 :
          partial_mean.append(float(s)/float(t))
        else:
          partial_mean.append(float('inf'))
      final_mean.append(partial_mean)
    return final_mean

  def generate_k_clusters(self,folder):
    pool = ThreadPool(cpu_count())
    result = pool.map(self.read_image, folder)
    pool.close()
    pool.join()
    self.cluster = [r[0] for r in result if r[0] != None]
    self.data = [r[1] for r in result if r[1] != None]
    self.end = [r[2] for r in result if r[2] != None]

  def rearrange_clusters(self):
    isover = False
    while(not isover):
      isover = True
      m = self.generate_k_means()
      for x in range(len(self.cluster)):
        dist = []
        for a in range(self.k):
            dist.append( self.manhattan_distance(self.data[x],m[a]) )
        _mindist = dist.index(min(dist))
        if self.cluster[x] != _mindist :
          self.cluster[x] = _mindist
          isover = False
    self.cluster_ACTcentroid = m

  def export_clusters(self):
    for k in range(self.k): #initialization
        self.cluster_data[k] = []
        self.cluster_IMGcentroid[k] = []
    for i in range(len(self.cluster)):
        self.cluster_data[self.cluster[i]].append(i)
    for key, values in self.cluster_data.items():
        print(key, values)
        act_centroid = self.cluster_ACTcentroid[key]
        min_dist = -1
        for img_idx in values:
            dist = self.manhattan_distance(self.data[img_idx], act_centroid)
            if min_dist < 0 or dist <= min_dist:
                min_dist = dist
                self.cluster_IMGcentroid[key] = img_idx
    print(self.cluster_IMGcentroid)


def groupimage(videoName, k):
    types = ('*.jpg', '*.JPG', '*.png', '*.jpeg')
    imagePaths = []
    video_folders = './data/rawData/'
    folder = os.path.join(video_folders, videoName, 'src')
    if not folder.endswith("/") :
        folder+="/"
    for files in types :
        imagePaths.extend(sorted(glob.glob(folder+files)))
    nimages = len(imagePaths)
    nfolders = int(math.log(k, 10))+1
    if nimages <= 0 :
        print("No images found!")
        exit()
    #pbar = tqdm(total=nimages)
    k = K_means(k,False,128)
    k.generate_k_clusters(imagePaths)
    k.rearrange_clusters()
    k.export_clusters()

    mainDir = os.getcwd()
    rawDataDir = os.path.join(mainDir, 'data', 'rawData')
    outputDir = os.path.join(rawDataDir, videoName)
    clust_data_file = os.path.join(outputDir, 'cluster_data_'+ str(k.k) +'.pk')
    clust_centroid_file = os.path.join(outputDir, 'cluster_centroid_' + str(k.k)+ '.pk')
    #pickle.dump(k.cluster_data, open(clust_data_file, 'wb')) # output the whole clustering result
    #pickle.dump(k.cluster_IMGcentroid, open(clust_centroid_file, 'wb')) #output img indices as clusters' centroids

    #clust_data = pickle.load(open(clust_data_file, 'rb'))
    #clust_centroid = pickle.load(open(clust_centroid_file, 'rb'))
    print(videoName, " is clustered!")
    return k.cluster_data, k.cluster_IMGcentroid

"""
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="path to image folder")
ap.add_argument("-k", "--kmeans", type=int, default=5, help="how many groups")
ap.add_argument("-r", "--resample", type=int, default=128, help="size to resample the image by")
ap.add_argument("-s", "--size", default=False, action="store_true", help="use size to compare images")
ap.add_argument("-m", "--move", default=False, action="store_true", help="move instead of copy")
args = vars(ap.parse_args())
types = ('*.jpg', '*.JPG', '*.png', '*.jpeg')
imagePaths = []
# input: ./data/rawData/
video_folders = args["folder"]
videoList = sorted(next(os.walk(video_folders))[1])
#for i, videoName in enumerate(videoList):
folder = os.path.join(video_folders, videoName, 'src')
print(folder)
if not folder.endswith("/") :
    folder+="/"
for files in types :
    imagePaths.extend(sorted(glob.glob(folder+files)))
nimages = len(imagePaths)
nfolders = int(math.log(args["kmeans"], 10))+1
if nimages <= 0 :
    print("No images found!")
    exit()
if args["resample"] < 16 or args["resample"] > 256 :
    print("-r should be a value between 16 and 256")
    exit()
pbar = tqdm(total=nimages)
k = K_means(args["kmeans"],args["size"],args["resample"])
k.generate_k_clusters(imagePaths)
k.rearrange_clusters()
k.export_clusters()
"""



#NOTE: modify
"""
for i in range(k.k) :
	try :
	  os.makedirs(folder+str(i+1).zfill(nfolders))
	except :
	  print("Folder already exists")
action = shutil.copy
if args["move"] :
	action = shutil.move
for i in range(len(k.cluster)):
	action(k.end[i], folder+"/"+str(k.cluster[i]+1).zfill(nfolders)+"/")
"""
