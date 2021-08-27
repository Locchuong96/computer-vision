import cv2 
import urllib.request
import numpy as np 
import matplotlib.pyplot as plt 
import time

class ipcam:

    def __init__(self,url,fx=0.5,fy=0.5):
        self.url = url
        self.fx  = fx 
        self.fy  = fy 

    def read(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()),dtype = np.uint8)
        img  = cv2.imdecode(imgNp,-1)
        imgResized = cv2.resize(img,(0,0),fx = self.fx, fy = self.fy)
        return imgResized