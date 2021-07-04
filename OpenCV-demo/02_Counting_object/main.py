# import your library
import cv2 
import matplotlib.pyplot as plt

cap = cv2.VideoCapture("camera2.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history = 100,varThreshold= 40)

while True:

    ret,frame = cap.read()
    # Get shape of frame
    #print(frame.shape)

    # Extract Region of interest

    #Apply Subtrackbackground for detect somthing moving
    roi = frame[0:767,0:1359]
    mask1 = object_detector.apply(roi)
    _,mask2 = cv2.threshold(mask1,20,25,cv2.THRESH_BINARY)

    #Blur 
    mask2 = cv2.medianBlur(mask2,21)
    
    # Find contours
    contours,_ =  cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    # find all contour all a frame
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 20:
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            detections.append([x,y,w,h])
    
    # Object Tracking
    for pos in detections:
        x,y,w,h = int(pos[0]),int(pos[1]),int(pos[2]),int(pos[3])
        cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),2)

    key = cv2.waitKey(1)
    #cv2.imshow("mask1",mask1)
    #cv2.imshow("mask2",mask2)
    cv2.imshow("frame",frame)
    #cv2.imshow("ROI",roi)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()