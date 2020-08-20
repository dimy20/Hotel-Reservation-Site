import time
import cv2
import numpy as np
from skimage.measure import ransac 
from skimage.transform import FundamentalMatrixTransform
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
#process each frame  
def process_frame(frame,w,h):
    res_frame= cv2.resize(frame,(w,h))  
    kps,matches= fe.extract(res_frame)
    #Draw circle for kps
    for kp in kps:
        u1,v1 = map(lambda x :(int(x)), kp.pt)
        res_frame = cv2.circle(res_frame,(u1,v1),1,(0,255,0),2)

    #Draw line for matching keypoints
    for m in matches:
        u2,v2 = map(lambda x : (int(x.pt[0]),int(x.pt[1])) ,m)
        res_frame = cv2.line(res_frame,u2,v2,(255,0,0),2)
    #res_frame = cv2.drawKeypoints(res_frame,kps,None,color=(0,255,0))
    return res_frame

def video_Init():
    cap = cv2.VideoCapture("production ID_4608595.mp4")
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//4)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)//4)
    cv2.namedWindow("test")
    cv2.moveWindow("test",0,0)
    while 1:
        success,img= cap.read()
        frame = process_frame(img,w,h)
            
        if (success):     
            cv2.imshow("test",frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'): 
            break
    cap.release() 
    cv2.destroyAllWindows()

fe = FeatureExtractor()
video_Init()
