import numpy as np 
import cv2
import cv2.aruco as aruco
import os
import ArucoModule as arm
import my_ivs


def main(): 

    my_dict = {
        0: "Heineken_can",`
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


    url_ip = "http://192.168.1.4:8080/shot.jpg"
    
    cap  = my_ivs.ipcam(url_ip,fx = 0.6,fy = 0.6)
    
    path = "D:/VV Solutions/project_VVSAUTO/aruco marker/decode"
    augDics = arm.loadAugImages(path)

    while True:
        img  = cap.read()
        arucoFound = arm.findArucoMarkers(img)

        # Loop through all the marker and agument each one
        if (len(arucoFound[0])) != 0:

            list_id = []

            for bbox,id in zip(arucoFound[0],arucoFound[1]):
                #print(bbox,id)
                #Check
                if int(id) in augDics.keys():
                    img = arm.augmentAruco(bbox,id,img, augDics[int(id)])
                    
                    list_id.append(int(id))

            cv2.putText(img,str("Total: {}".format(len(list_id))),(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

            pos_x = 60
            pos_y = 60

            for i in range(20):
                label = my_dict[i]
                number = list_id.count(i)
                if number > 0:
                    cv2.putText(img, str(" {}: {}".format(label,number)) ,(pos_x,pos_y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,210,0),2)
                    pos_y += 20


        cv2.imshow("img",img)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()