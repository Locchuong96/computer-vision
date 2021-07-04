import cv2

import PIL.Image
import PIL.ImageTk

import tkinter as tk
from tkinter import *

import datetime

import pytesseract

path_icon = "D:/VV Solutions/project_VSSOCR/VVS.ico"
path_save = "./cap_img"
cam 	  = cv2.VideoCapture(1,cv2.CAP_DSHOW)
photo     = None
frame     = []
frame_cap = []

def update(period = 100):

	global cam,photo,frame
	
	ret, frame = cam.read()  #Update frame cap
	frame_inv = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_inv))

	my_canvas.create_image(25,20,image = photo, anchor = tk.NW)
	window_home.after(period,update)

def capture():

	global photo,frame,frame_cap

	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
	
	frame_cap = frame

	hImg,wImg,_ = frame_cap.shape

	boxes = pytesseract.image_to_data(frame_cap)

	for x,b in enumerate(boxes.splitlines()):
	    if x!= 0:
	        b = b.split()
	        #print(b)
	        if len(b) == 12:
	            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
	            cv2.rectangle(frame_cap,(x,y),(w+x,h+y),(0,0,255),1)
	            cv2.putText(frame_cap,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,0.3,(255,0,0),1)

	cv2.imshow("Capture",frame_cap)

def save():
	
	global frame_cap
	
	time = str(datetime.datetime.now()).replace(":","-")
	cv2.imwrite(path_save +"/" +time + ".jpg",frame_cap)

#Create window home
window_home = tk.Tk()
window_home.geometry("700x600")
window_home.title("camera python")
window_home.iconbitmap(path_icon)
window_home.resizable(width = False, height = False)

#Create canvas
my_canvas = tk.Canvas(window_home,width = 700, height = 600, bd = 0, highlightthickness = 0)
my_canvas.pack(fill = "both", expand = True)

#create a button
bt_cap = tk.Button(window_home,text = "Capture",command = capture)
my_canvas.create_window(300,540,anchor = "nw",window = bt_cap)

bt_save = tk.Button(window_home,text = "Save",command = save)
my_canvas.create_window(380,540,anchor = "nw",window = bt_save)

update()
window_home.mainloop()
cam.release()
