import cv2
from skimage.measure import ransac 
from skimage.transform import FundamentalMatrixTransform
import numpy as np
class FeatureExtractor(object):
    def __init__(self):
        # orb nad brute force matcher algorithim
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.last = None
   
    def extract(self,frame):
        #extract features
        features = cv2.goodFeaturesToTrack(np.mean(frame,axis=2).astype(np.uint8),maxCorners=3000, qualityLevel=0.01,minDistance=3)
        kps = [cv2.KeyPoint(x = f[0][0], y = f[0][1], _size=10) for f in features]
        # compute descriptors 
        kps, des = self.orb.compute(frame,kps) 
        # get matching features
        
        res = []
        ptsRight = []
        ptsLeft = [] 
        matches = None
        if self.last is not None:
            matches = self.bf.knnMatch(des,self.last['des'],k=2)
            for m,n in matches:
                if (m.distance < 0.75*n.distance):
                    kp1 = kps[m.queryIdx]
                    kp2 = self.last['kps'][m.trainIdx]
                    ptsLeft.append(self.last['kps'][m.trainIdx].pt)
                    ptsRight.append(kps[m.queryIdx].pt)
                    res.append((kp1,kp2))

        self.last = {'kps': kps, 'des' : des}
        #Filtering - removers shitty matches
        
        res = np.array(res) 
        if (len(res)> 0):
            ptsLeft = np.int32(ptsLeft)
            ptsRight = np.int32(ptsRight)
         
            model,inliers = ransac((ptsLeft,ptsRight),
            FundamentalMatrixTransform,
            min_samples =8,
            residual_threshold=1,
            max_trials=100)
        
            res = res[inliers]
        
        #returns filtered matching keypoints 
        return kps,res 
#
