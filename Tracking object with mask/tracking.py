
import cv2 
import time

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# Faster
#tracker = cv2.legacy_TrackerMOSSE.create()
#Lower but more accuracy
tracker = cv2.legacy_TrackerCSRT.create()
time.sleep(3)
ret,frame = cap.read()
bbox = cv2.selectROI("Tracking",frame,False)
tracker.init(frame,bbox)

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(frame,"Tracking",(50,75),cv2.FONT_HERSHEY_COMPLEX,
                0.7,(0,255,0),1)

while True:

    ret,frame = cap.read()

    success,bbox = tracker.update(frame)
    #print(bbox)

    if success:
        drawBox(frame,bbox)
    else:
        cv2.putText(frame,"LOST",(50,75),cv2.FONT_HERSHEY_COMPLEX,
                    0.7,(0,255,0),1)

    timer = cv2.getTickCount()

    fps = cv2.getTickFrequency()/(cv2.getTickCount() - timer)
    
    cv2.putText(frame,"fps: {}".format(str(fps)),(50,50),cv2.FONT_HERSHEY_COMPLEX,
                0.7,(0,255,0),1)

    cv2.imshow("gotcha",frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()