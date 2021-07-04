import numpy as np 
import cv2
import cv2.aruco as aruco
import os

my_dict = {
0: "Heineken_can",
1: "Heineken_bottle",
2: "Tiger_can",
3: "Cocacola_can",
4: "Cocacola_bottle",
5: "Pepsi_can",
6: "Pepsi2_can",
7: "Tide_bottle",
8: "Tide_package",
9: "Omo_package",
10: "Omo2_package",
11: "Sunlight_bottle",
12: "Sunlight_package",
13: 'Colgate_tube',
14: 'Colgate2_tube',
15: 'Namhuong_bottle',
16: 'Olive_bottle',
17: 'Lifebouy',
18: 'Lays',
19: 'Head&Shower',
}

def loadAugImages(path):
    myList = os.listdir(path)
    noOfMarkers = len(myList)
    print("Total Number detected: ",noOfMarkers)
    augDics = {}
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0]) # Get the id
        imgAug = cv2.imread(f'{path}/{imgPath}')
        augDics[key] = imgAug #Create a dict with img face
    return augDics

def findArucoMarkers(img, markerSize = 4, totalMarkers =250, draw = True): # 6x6
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Define which dict
    #arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    key = getattr(aruco,f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs,ids,rejected = aruco.detectMarkers(imgGray,arucoDict, parameters = arucoParam)
    #print(type(ids)) None array object
    #print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)

    return [bboxs,ids]

def augmentAruco(bbox,id,img,imgAug,drawId = True ):
    #topleft
    tl = bbox[0][0][0],bbox[0][0][1]
    #topright
    tr = bbox[0][1][0],bbox[0][1][1]
    #bottomright
    br = bbox[0][2][0],bbox[0][2][1]
    #bottomleft
    bl = bbox[0][3][0],bbox[0][3][1]

    #Get the size
    h,w,c = imgAug.shape

    #Get point and matrix
    pts1 = np.array([tl,tr,br,bl])
    pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])
    matrix, _ = cv2.findHomography(pts2,pts1)
    # the image where you get a img
    imgOut = cv2.warpPerspective(imgAug,matrix,(img.shape[1],img.shape[0]))
    # the image where you get anything but the blackholes
    cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))

    imgOut = img + imgOut

    if drawId:
        cv2.putText(imgOut,my_dict[id[0]],tl,cv2.FONT_HERSHEY_SIMPLEX,0.3,(200,200,0),1)
    return imgOut

