import cv2 
import numpy as np 

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#params for Shitomashi corner detection
feature_params = dict(maxCorners = 100,
                    qualityLevel = 0.3,
                    minDistance = 7,
                    blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict(winSize = (15,15),
                maxLevel = 2,
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))


#Take the first frame and find corners in it
old_ret,old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray,mask = None, **feature_params)


#Create a mask image for drawning purposes
mask = np.zeros_like(old_frame)

# Set function mouse click
def reset_game(event,x,y,flags,params):
    global old_ret,old_frame,old_gray,p0,mask
    if event == cv2.EVENT_RBUTTONDBLCLK:
        old_ret,old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray,mask = None, **feature_params)
        mask = np.zeros_like(old_frame)

#Create a windownamed
cv2.namedWindow("img")
cv2.setMouseCallback("img",reset_game)
while old_ret:
    
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    p1,st,err = cv2.calcOpticalFlowPyrLK(old_gray,frame_gray,p0,None, **lk_params)

    #Select good points
    try:
        good_new = p1[st == 1] # turn float point into int0 point
        good_old = p0[st == 1]
    except: pass
    
    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        x_new,y_new = new.ravel()
        x_old,y_old = old.ravel()
        mask = cv2.line(mask,(x_new,y_new),(x_old,y_old),(255,0,0),2)
        frame = cv2.circle(frame,(x_new,y_new),5,(0,0,255),-1)
    
    img = cv2.add(frame,mask)

    if good_new.shape[0] > 0:
        cv2.putText(img,"No: {}".format(good_new.shape[0]),(10,20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
    elif good_new.shape[0] == 0:
        cv2.putText(img,"You Win!",(10,20),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
    
    cv2.imshow("img",img)


    #Update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

    key = cv2.waitKey(10)
    if key == 27: break

cap.release()
cv2.destroyAllWindows()
