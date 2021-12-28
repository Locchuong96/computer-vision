'''
Adaptive thresholding

https://www.pyimagesearch.com/2021/05/12/adaptive-thresholding-with-opencv-cv2-adaptivethreshold/

In the previous section, we used a global value as threshold value. But it may not be good in all the conditions where
image has different lighting conditions in different areas. In that case, we go for adaptive thresholding. In this, the
algorithm calculate the threshold for a small regions of the image. So we get different thresholds for different regions
of the same image and it gives us better results for images with varying illumination.
It has three ‘special’ input params and only one output argument.

• cv2.ADAPTIVE_THRESH_MEAN_C : threshold value is the mean of neighbourhood area.
• cv2.ADAPTIVE_THRESH_GAUSSIAN_C : threshold value is the weighted sum of neighbourhood values where weights are a gaussian window
'''
import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

bg = cv2.imread('./matrix.jpg')

ret,frame = cap.read()

while ret:

	ret,frame = cap.read()
	
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	blurred = cv2.GaussianBlur(gray, (7, 7), 0)

	#print(gray.shape) # (480,640)

	thresh = cv2.adaptiveThreshold(blurred, 255,
	cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21, 10)

	#print(cv2.bitwise_and(bg[:,:,1],thresh))

	cv2.imshow("frame",thresh)

	if cv2.waitKey(1) == 27:
		break 

cap.release()

cv2.destroyAllWindows()