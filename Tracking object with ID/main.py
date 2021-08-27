import cv2 
import tracker

detector_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Createa your tracker
ct = tracker.CentroidTracker()

while True:
    #Create a rects
    rects = []
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    object_cascade = detector_cascade.detectMultiScale(gray,scaleFactor= 1.1, minNeighbors = 5)

    #Remember you are working each frame

    for x,y,w,h in object_cascade:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        rects.append((x,y,(x+w),(y+h)))

    try:
        objects = ct.update(rects)
    except: pass

    for (objectID,centroid) in objects.items():
        text = "ID {}".format(objectID)
        cv2.putText(frame,text,(centroid[0]-10,centroid[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        cv2.circle(frame,(centroid[0],centroid[1]),4,(0,255,0),-1)

    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
