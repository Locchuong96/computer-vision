import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

ret,frame = cap.read()

while ret:

	ret,frame = cap.read()

	cv2.imshow("frame",frame)

	if cv2.waitKey(1) == 27:
		break 

cap.release()

cv2.destroyAllWindows()