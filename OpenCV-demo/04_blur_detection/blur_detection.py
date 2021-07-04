url_ip = "http://192.168.1.24:8080/shot.jpg"
cam1  = ipcam(url_ip,fx = 0.35,fy = 0.35)

# Subtractors
mog2Subtractor = cv2.createBackgroundSubtractorMOG2(1,500, False) #Biger var threshold, time decrease will faster
moving = False
pic = None

while True:

    frame1 = cam1.read()
    mog2Mmask = mog2Subtractor.apply(frame1)

    total_mog2 = np.sum(mog2Mmask)
    #cv2.putText(mog2Mmask,"total: {}".format(total_mog2), (10,20),cv2.FONT_HERSHEY_COMPLEX, 0.5,(255,255,255),1)
    cv2.putText(frame1,"total: {}".format(total_mog2), (200,20),cv2.FONT_HERSHEY_COMPLEX,
                0.5,(255,255,255),1)

    if total_mog2 > 1000000:
        cv2.putText(frame1,"MOVING".format(total_mog2), (10,20),cv2.FONT_HERSHEY_COMPLEX,
                    0.75,(0,0,255),1)
        moving = True
    else:
        cv2.putText(frame1,"STATIC".format(total_mog2), (10,20),cv2.FONT_HERSHEY_COMPLEX,
                    0.75,(0,255,0),1)
        moving = False
    
    cv2.imshow('Original', frame1)
    #cv2.imshow('MOG2', mog2Mmask)
    
    cv2.moveWindow('Original',0, 50)

    key = cv2.waitKey(1)

    if key == ord("c"):
        pic = frame1

        if moving == True:
            cv2.putText(pic,"BLUR".format(total_mog2), (10,40),cv2.FONT_HERSHEY_COMPLEX, 
                        0.75,(0,0,255),1) 
        else:
            cv2.putText(pic,"NO BLUR".format(total_mog2), (10,40),cv2.FONT_HERSHEY_COMPLEX, 
                        0.75,(0,255,0),1)
        
        cv2.imshow("Picture",pic)
        cv2.moveWindow('Picture', 680, 50)
    
    elif key == ord("x"):
        cv2.destroyWindow("Picture")
    
    elif key == 27:
        break
    
cv2.destroyAllWindows()