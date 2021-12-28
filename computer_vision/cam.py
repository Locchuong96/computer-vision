'''
Thresholding
if the value is greater than a threshold value, it is assigned one value (may be white)
if it is assigned another value (may be black)
The function used is cv2.threshold
		first argument is source image, must be in grayscale 
		second value is the threshold value, which is used to classify the pixel values
some style of threshold
		. cv2.THRESH_BINARY
		. cv2.THRESH_BINARY_INV
		. cv2.THRESH_BINARY_TRUNC
		. cv2.THRESH_TOZERO
		. cv2.THRESH_TOZERO_INV
'''
import cv2
import numpy as np 

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

bg = cv2.imread('./matrix.jpg')

ret,frame = cap.read()

while ret:

	ret,frame = cap.read()
	
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	gray = cv2.medianBlur(gray,1)

	#print(gray.shape) # (480,640)

	ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

	# thresh = np.array(thresh)
	# thresh = thresh /255
	# thresh = thresh.astype(np.int32)

	b  = bg[:,:,0]
	g  = bg[:,:,1]
	r  = bg[:,:,2]

	img = np.zeros_like(frame)

	#img = np.hstack((thresh * b,thresh * g,thresh * r))
	#img = np.vstack((thresh * b,thresh * g,thresh * r))

	img[:,:,1] = thresh * b
	img[:,:,0] = thresh * g
	img[:,:,2] = thresh * r

	#print(img.shape)

	result =cv2.addWeighted(bg,0.5,img,0.5, 0.0)

	cv2.imshow("frame",result)

	if cv2.waitKey(1) == 27:
		break 

cap.release()

cv2.destroyAllWindows()