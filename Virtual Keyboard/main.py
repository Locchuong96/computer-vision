import cv2 
import mediapipe
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pynput.keyboard import Controller

#create a controller ketboard
keyboard = Controller()

#create a detector
detector = HandDetector(detectionCon = 0.8)
#print(detector)

cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,607)

#create a class for button
class Button():
	def __init__(self,pos,text, size = (70,70),button_color = (255,200,0)):
		self.pos = pos    # position x,y
		self.size = size  # deltax,deltay
		self.text = text  # text
		self.button_color = button_color

	def draw(self,frame):
		x,y = self.pos 
		w,h = self.size
		#method draw for the current frame
		cv2.rectangle(frame,(x,y),(x+w,y+h),self.button_color,cv2.FILLED)
		cv2.putText(frame,self.text,(x+10,y+40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)

#create a button list
buttonList = []

ltext = ["Q","W","E","R","T","Y","U","I","O","P", 
			"A","S","D","F","G","H","J","K","L",";",
				"Z","X","C","V","B","N","M",",",".","/"]

pos_zero = (70,70)

for i,text in enumerate(ltext):
	if i < 10:
		buttonList.append(Button( (pos_zero[0]+i*100,pos_zero[1]),text) )
	if i < 20 and i>9:
		buttonList.append(Button( (pos_zero[0]+(i-10)*100,pos_zero[1]+90),text) )
	if i < 30 and i >19:
		buttonList.append(Button( (pos_zero[0]+(i-20)*100,pos_zero[1]+180),text) )

#finalText
finalText = ":"

#transparent
alpha = 0.5

while True:	

	ret,frame = cap.read()

	#flip the frame
	frame = cv2.flip(frame,1)

	#draw landmask on frame
	frame = detector.findHands(frame)

	#get landmask list of point and bboxInfo coner of the rectangle and the cener
	lmList,bboxInfo = detector.findPosition(frame)

	#create black frame 
	black_frame = np.zeros_like(frame,np.uint8)

	#draw keyboard 
	for button in buttonList:
		
		#draw button and check by loop over very button
		button.draw(black_frame)

		#get button size
		x,y = button.pos 
		w,h = button.size

		#check lmlsit
		if lmList:
			if (x< lmList[8][0]<x+w) and (y< lmList[8][1]<y+h):
				button.button_color = (255,0,0)
				# find distance between 8 and 12 point
				l,_,_ = detector.findDistance(8,12,frame)
				# if the distance smaller than a value
				if l < 60:
					button.button_color = (255,200,255)
					finalText = finalText + button.text
					keyboard.press(button.text)
					#sleep abit

			else:
				button.button_color = (255,200,0)
		else:
			button.button_color = (255,200,0)

	#add the frame
	out =frame.copy()
	#create a mask 0,1 with the drawed black_frame
	mask = black_frame.astype(bool)
	#add weight current frame and the black frame witht the alpha
	out[mask] = cv2.addWeighted(frame,alpha,black_frame,1-alpha,0)[mask]

	#draw the text
	cv2.rectangle(out,(50,400),(400,450),(255,200,100),cv2.FILLED)
	cv2.putText(out,finalText,(60,440),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)

	cv2.imshow("Frame",out)
	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
