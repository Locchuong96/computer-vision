import cv2
import numpy as np

img = cv2.imread("./marcus.jpg")
#print(img.shape)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

blurred  =cv2.GaussianBlur(gray, (7, 7), 1)

ret,thresh = cv2.threshold(blurred,100,255,cv2.THRESH_BINARY)
print(thresh.shape)

bg = cv2.imread('./bg3.png')
#print(bg.shape)

b  = bg[:,:,0]
g  = bg[:,:,1]
r  = bg[:,:,2]

fg = np.zeros_like(img)
#print(fg.shape)

fg[:,:,1] = thresh * b
fg[:,:,0] = thresh * g
fg[:,:,2] = thresh * r

result =cv2.addWeighted(bg,0.3,fg,0.7, 0.0)

while True:

	cv2.imshow("result",result)

	if cv2.waitKey(1) == 27:
		break


cv2.imwrite("result.jpg",result)

print('Save done')
cv2.destroyAllWindows()

