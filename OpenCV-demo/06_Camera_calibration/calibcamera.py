import numpy as np 
import cv2 
import cv2.aruco as aruco

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

dictionary = cv2.aruco.getPredefinedDictionary(10)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

while True:
	ret,frame = cap.read()

	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

	bbox,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray,dictionary)

	if ids is not None:

		cv2.aruco.drawDetectedMarkers(frame,bbox,ids)

	# If found, add object points, image points (after refining them)
	if ret == True:

		objpoints.append(objp)
		cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners)
		# Draw and display the corners
		cv2.drawChessboardCorners(frame, (5,4), corners,ret)

		retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


	cv2.imshow("frame",frame)

	key = cv2.waitKey(1)

	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()