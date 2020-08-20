import time
import cv2
import numpy as np
from skimage.measure import ransac 
from skimage.transform import FundamentalMatrixTransform
from FeatureExtractor import FeatureExtractor
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
