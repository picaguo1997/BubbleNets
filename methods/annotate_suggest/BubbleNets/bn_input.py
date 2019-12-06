import cPickle as pickle
import tensorflow as tf
import numpy as np
import os
import random
import IPython
import math

class BN_Input:
	def __init__(self, vector_file, n_ref=3):
		self.vectors = pickle.load(open(vector_file,'rb'))['frame_resnet_vectors']
		self.n_ref = n_ref
		self.n_frames, self.vector_dim = self.vectors.shape

	def video_batch_n_ref_no_label(self, vid_name, idx0, idx1, batch=5):
		# Used during implementation for forming video consensus.
		n_in_frames = self.n_ref + 2 #5
		vector_tensor = np.zeros(shape=(batch, n_in_frames *
										(self.vector_dim + 1)), dtype=np.float32)
		idx_np = np.zeros(n_in_frames) #5

		# Make sure comparison frames are not used for reference.
		idx_cand = range(self.n_frames)
		if idx0 < idx1: del idx_cand[idx1]; del idx_cand[idx0]
		else: del idx_cand[idx0]; del idx_cand[idx1]

		# Select random reference frames and output network input tensor.
		for i in range(batch):
			if n_in_frames <= self.n_frames-2:
				#change
				mainDir = '/Users/yhkuo/BubbleNets'
				resultDir = os.path.join(mainDir, 'Configurations', 'clustering_3.pk')
				clusters = pickle.load(open(resultDir, 'rb'))
				target = []
				for item in clusters:
					if item[0] == vid_name:
						target = item[2] #centroids
						break
				idx_test = []
				for idx in target:
					idx_test.append(idx)
				#idx = random.sample(idx_cand,self.n_ref)
			else: # Use replacement for small videos.
				idx = [random.choice(idx_cand) for _ in range(self.n_ref)]
			idx = [idx0, idx1, idx_test[0], idx_test[1], idx_test[2]]
			idx_np[:] = idx
			vector_diff = np.concatenate((self.vectors[idx].flatten(),
														idx_np/self.n_frames))
			vector_tensor[i] = vector_diff
		return vector_tensor
