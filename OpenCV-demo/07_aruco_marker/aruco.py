import numpy as np 
import cv2
import cv2.aruco as aruco
import os
import ArucoModule as arm

def main(): 
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    path = "D:/VV Solutions/project_VVSAUTO/aruco marker/decode"
    augDics = arm.loadAugImages(path)

    while True:
        success,img  = cap.read()
        arucoFound = arm.findArucoMarkers(img)

        # Loop through all the marker and agument each one
        if (len(arucoFound[0])) != 0:
            for bbox,id in zip(arucoFound[0],arucoFound[1]):
                #print(bbox,id)
                #Check
                if int(id) in augDics.keys():
                    img = arm.augmentAruco(bbox,id,img, augDics[int(id)])
                    #augmentAruco(bbox,id,img, imgAug)

        cv2.imshow("img",img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()