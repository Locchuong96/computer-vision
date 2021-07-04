import serial
import time 
import datetime
import dlib 
import face_recognition
import cv2 
import pandas as pd 
import numpy as np 
import os 
import tkinter as tk 
from tkinter import * 
import PIL.Image
import PIL.ImageTk
from threading import Thread 
import sqlite3 
import json
import base64
import requests
import sys
import eventlet

"""
18/5/21 Build function capture the last image and reset if video connect interrupted
"""
path_storage         = "./vvsac 1.0/storage/" # storage variable for communicate,  last image

"""
6/5/21 Write function build API
"""
path_erp = "./vvsac 1.0/erp_data/erp_hr2.csv"
url_api  = "http://erp-exp.vastbit.com/api/services/app/EmployeeAttendance/CheckIn"
df_erp   = pd.read_csv(path_erp)

path_icon = "./vvsac 1.0/files/" # path follow to icon floder for using these file in this floder
path_id   = r"./vvsac 1.0/face_Id" # path follow to face floder, this is available face
cap       = cv2.VideoCapture(0,cv2.CAP_DSHOW) # Make a connection into the webcam
photo     = None # This is every important, tkinter image using this variable to display   

path_csv      = "./vvsac 1.0/csv_Daily/" # This is for create database and storage everytime turn on detect mode, path follow to icon floder for csv
path_db       = "./vvsac 1.0/DB_Daily/" # This is for create database and storage everytime turn on detect mode, path follow to icon floder for database
file_name_db  = str("") # This is for create database and storage everytime turn on detect mode, the name of file database
file_name_csv = str("") # This is for create database and storage everytime turn on detect mode, the name of csv file
conn          = None # This is for create database and storage everytime turn on detect mode, Create this connect into database
df            = pd.DataFrame(None,columns = ["Name","Date","Time","Distance"]) # This is for create database and storage everytime turn on detect mode,  Create dataframe for csv file

accept_distance  = 0.4 # Accept rate for detect mode 
face_locations   = []  # store all face's locations detected in frame in a list
face_encodings   = []  # store all's encode detected in frame in a list

time_off  = "19:01" # This function is use to set time of for your code

name_now  = str("") # This function is use for storage detecting name, for comparing each period, for trigger new face event
name_prev = str("") # This function is use for storage detected name, detecting compare with this name, if 's the same, then don't do anything new
dis_val   = 0.0 

thresh_x     = 70  # For crop ROI face  to storage
thresh_y     = 100 # For crop ROI face to storage
path_unknown = "./vvsac 1.0/face_Unknown/" # Path store unknown faces
path_known   = "./vvsac 1.0/face_Known/" # Path store known face

"""
19/5/21 Build function capture the last image and reset if video connect interrupted
"""
eventlet.monkey_patch()

"""
19/5/21 Build function capture the last image and reset if video connect interrupted
"""
def restart():
	print("argv was",sys.argv)
	print("sys.executable was", sys.executable)
	print("restart now")
	os.execv(sys.executable, ['python'] + sys.argv)

# This function is using to support face_list function, to find the name in image path
def find_name(path):
	end_index  = path.index(".jpg")
	start_index = path.index("\\")

	return path[start_index+1:end_index]

# This function access into given path and make two list, one for know_faces names and one for these face encoding 
def face_list(path):
	known_face_paths     = []                               # list of known path
	known_face_names     = []                               # list of known names
	known_face_encodings = []                               # list of encodings
	known_face_images    = []                               # list of known faces
	dirs = os.listdir(path)

	for direc in dirs:
		img_path = os.path.join(path,direc)                 # Read img path
		known_face_paths.append(img_path)                   # Append img path
		face = face_recognition.load_image_file(img_path)   # Read img in img_path
		known_face_images.append(face)                      # Append images face
		encoding = face_recognition.face_encodings(face)[0] # Encoding face
		known_face_encodings.append(encoding)               # Append encoding list
		name = find_name(img_path)                          # Find name of image
		known_face_names.append(name)                       # Append name to name list


	return known_face_names,known_face_encodings

#This function is use for create database and dataframe
def funct_datacreate():
	
	global path_csv, path_db, file_name_db, file_name_csv, conn, df

	t= datetime.datetime.now()
	time_name =str(t)[0:10].replace(":","-")     # Change your time index here
	file_name_csv = "VVSAC_" + time_name + ".csv"
	file_name_db  = "VVSAC_" + time_name + ".db"
	print(str(datetime.datetime.now()) + " CHECKING DATA...")
	# time_off = str(t)[11:16]
	# if time_off == "11:02":
	# 	print("yes")

	#Create Dataframe
	if not os.path.exists(path_csv + file_name_csv):
		data = None
		df = pd.DataFrame( data,columns = ["Name","Date","Time","Distance"] )	
		df.to_csv(path_csv + file_name_csv)
		print(file_name_csv + " : Created!")
	else:
		# IF exist the dataframe it will read the dataframe in this folder
		print(file_name_csv + " Already!")
		df = pd.read_csv(path_csv + file_name_csv)

	# Create Database
	if not os.path.exists(path_db + file_name_db):
		conn = sqlite3.connect(path_db + file_name_db)
		c = conn.cursor()
		# Create table could be make mistake if you table allready there
		c.execute(""" 
			CREATE TABLE table_io
			(Name TEXT,
			Date TEXT,
			Time TEXT,
			Distance REAL)
			""")
		conn.commit()
		conn.close()
		print(file_name_db +  "  : Created!")
	else:
		# IF exist the database then print out notification and pass
		print(file_name_db + " Already!")
	
	return

def add_face():
	
	global  path_csv,path_db,file_name_csv,file_name_db,conn,df,name_now,dis_val

	t = datetime.datetime.now()
	time_now = str(t)

	#Value add to dataframe and database
	date_clock = time_now[0:10]
	time_clock = time_now[11:-1]
	name       = name_now
	dis        = dis_val

	#Add dataframe
	df1  = pd.DataFrame({"Name":[name],"Date":[date_clock],"Time":[time_clock],"Distance":[dis]})
	df   = df.append(df1)
	df.reset_index(drop = True, inplace= True)
	df.to_csv(path_csv + file_name_csv)

	#Add database
	data_row = (name,date_clock,time_clock,dis)
	conn     = sqlite3.connect(path_db + file_name_db)
	c        = conn.cursor()
	c.execute("INSERT INTO table_io VALUES (?,?,?,?)",data_row)
	conn.commit()
	conn.close()

	return

def send_api(url,df,name,time,face):
	"""
	6/5/21 Write function build API
	"""

	header_dict = {"deviceId": "D0-37-45-F6-E1-21"}

	# decode face and turn it into base64 format
	ret,buf = cv2.imencode(".jpg",face)
	byte    = base64.b64encode(buf)
	content = str(byte)[2:-1]

	# make ajson file
	data = {
		  "employeeCode": df.loc[df["face_name"]== name,"employee_code"].values[0],
		  "timestamp"   : time.isoformat(),
		  "imageBlob"   : content
		}

	# Send API
	with eventlet.Timeout(1):
		rep = requests.post(url, json = data, headers = header_dict)
		
	#print(rep)
	#print( df.loc[df["face_name"]== name,"employee_code"].values[0] )

#Check date in Week before start to do anything
date_name = time.ctime()[:3]
# Create database and dataframe, everyday it will call this function one time and create the database and dataframe
# If Something wrong, you have to execute this file twice, then just read all data database and dataframe existed and go on
# This function just execute one time everytime open this script
funct_datacreate()
if (date_name == "Sat") or (date_name == "Sun"):

	print("Oops, today's {}, i am not working, Shutdown now!, Bye Bye".format(date_name))
	os.system('shutdown -s')

# Read all your face in face_Id floder and encode it
known_face_names,known_face_encodings = face_list(path_id)

# Create a window
window_detect = tk.Tk()
window_detect.geometry("1302x681+100+50") # 8-6-21 fix geometry display window (windown_widthxwindow_height+pixel_left+ pixel_down)
window_detect.title("Detect Window")
window_detect.iconbitmap(path_icon + "VVS.ico")
window_detect.resizable(width = False,height = False)

# 7/6/21 Make the window jump above all 
window_detect.attributes('-topmost',True)

# Define background 
bg_detect = PIL.ImageTk.PhotoImage(file = path_icon + "detect1.jpg")

# Define_Canvas
my_canvas = tk.Canvas(window_detect, width = 1302, height = 681, bd =0, highlightthickness = 0)
my_canvas.pack(fill = "both", expand = True)

# Put background into your canvas
my_canvas.create_image(0,0,image = bg_detect,anchor = "nw")

#Draw somthing on cavnvas first
label_time = tk.Label(window_detect, text = "Time"        	   , fg = "red"  , font = ("Arial",27)) # Label to say hello to the detected name
label_info = tk.Label(window_detect, text = "Say hello"        , fg = "green", font = ("Arial",27)) # Label to say hello to the detected name
label_prev = tk.Label(window_detect, text = "Previous Face: "  , fg = "green", font = ("Arial",20)) # Label info Previous face
label_now  = tk.Label(window_detect, text = "Now Face: "       , fg = "green", font = ("Arial",20)) # Label info Now face
val_prev   = tk.Label(window_detect, text = "Previous Name"    , fg = "green", font = ("Arial",20)) # Label display previous name od face
val_now    = tk.Label(window_detect, text = "Now Name"         , fg = "green", font = ("Arial",20)) # Label display now name of face

my_canvas.create_window(580,420,anchor = "nw", window = label_info)
my_canvas.create_window(450,520,anchor = "nw", window = label_time)
#my_canvas.create_window(400,500,anchor = "nw", window = label_prev)
#my_canvas.create_window(400,580,anchor = "nw", window = label_now)
#my_canvas.create_window(700,500,anchor = "nw", window = val_prev)
#my_canvas.create_window(700,580,anchor = "nw", window = val_now)

def update(period = 100):

	global cap,photo,path_id,face_locations,face_encodings,accept_distance,time_off,name_prev,name_now,dis_val,thresh_x,thresh_y,path_unknown,path_known
	global url_api,df_erp
	global path_storage,count_period_alive

	# Check time in every period, if this is time off, shutdown your system
	t        = datetime.datetime.now() # Get your time first
	label_time.configure(text = str(t))
	time_now = str(t)[11:16]

	if time_now == time_off:
		# print("YES")
		os.system('shutdown -s')

	# 18/5/21 fix bug 
	# Read new frame in cap connection and get face's location and face's encoding
	try:
		ret,frame      = cap.read()
		frame_cop      = frame.copy()

	except:
		# frame_cop      = frame.copy()
		restart()

	#cv2.imwrite(path_storage + "last_image.png",frame_cop) # writedown the last image 

	face_locations = face_recognition.face_locations(frame)
	face_encodings = face_recognition.face_encodings(frame,face_locations)

	# If detected some face then execute this code below
	if(len(face_locations) !=0):
		# Better put all this code bellow in try because sometime it's doesn't  catch up the face, i guess
		try:		
			for (top,right,bottom,left),face_encoding in zip(face_locations,face_encodings):
				# See if face is a match for known faces
				name             = "Unknown"
				# Compare known face encoding and unknown face encodning
				matches          = face_recognition.compare_faces(known_face_encodings,face_encoding)
				# Find the distance between these face
				face_distances   = face_recognition.face_distance(known_face_encodings,face_encoding)
				# Return Best index match, the lowest
				best_match_index = np.argmin(face_distances)
				
				# If matches at best_match_index is True anf face_distance lower than a accept_distance
				if matches[best_match_index] and face_distances[best_match_index] < accept_distance:
					# Name = name of face
					name     = known_face_names[best_match_index] + " " + str(round(face_distances[best_match_index],2))
					# Draw a rectangle
					frame    = cv2.rectangle(frame,(left,top),(right,bottom),(0,255,255),3)
					# Put the name in the text
					frame    = cv2.putText(frame,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
					# Crop ROI face
					roi_face = frame_cop[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]

					# Do something after detect, add to dataframe,database, save image
					t          = datetime.datetime.now() 
					time_now   = str(t)
					date_clock = time_now[0:10]
					time_clock = time_now[11:-1]
					name_prev  = name_now
					name_now   = known_face_names[best_match_index]
					dis_val    = round(face_distances[best_match_index],2)

					val_prev.configure(text = name_prev)
					val_now.configure(text = name_now)
					label_info.configure(text = "Hello " + name_now + " !")

					#This is for trigger event, if now doesn't like prev name then start to execute
					if name_prev != name_now:

						add_face()

						# 6/5/21 Write function build API
						# roi_face turn into frame for API
						# name_now for API
						# t for API

						#19/5/21 down server fault
						send_api(url_api,df_erp,name_now,t,roi_face)
						
						# Save this image to face_known
						img_path = path_known + known_face_names[best_match_index] +"_"+ date_clock.replace(":","-") + "_"+ time_clock.replace(":","-") + ".jpg"
						# Save your image
						cv2.imwrite(img_path,roi_face)
				
				# This else standfor if you don't see any face accepted then execute the code below
				else:
					# Draw a rectangle
					frame    = cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),3)
					# Put the name in the text
					frame    = cv2.putText(frame,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)
					# Crop ROI face
					roi_face = frame_cop[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]

					# Do something after detect, add to dataframe,database, save image
					t          = datetime.datetime.now()
					time_now   = str(t)
					date_clock = time_now[0:10]
					time_clock = time_now[11:-1]
					name_prev  = name_now
					name_now   = "Unknown"
					dis_val    = round(face_distances[best_match_index],2)

					val_prev.configure(text = name_prev)
					val_now.configure(text = name_now)
					label_info.configure(text = "Sorry, please try again!")

					#This is for trigger event, if now doesn't like prev name then start to execute
					if name_prev != name_now:

						# 6/5/21 Write function build API
						# roi_face turn into frame for API
						# name_now for API
						# t for API

						add_face()

						#19/5/21 down server fault
						send_api(url_api,df_erp,name_now,t,roi_face)

						# Save this image to face_known
						img_path = path_unknown + "Unknown_" + date_clock.replace(":","-")  +"_"+ time_clock.replace(":","-") + ".jpg"
						# Save your image
						cv2.imwrite(img_path,roi_face)
		except:
			pass
	
	# This else standfor detected no face
	else:
		name_prev                 = name_now
		name_now                  = "No face"
		val_prev.configure(text   = name_prev)
		val_now.configure(text    = name_now)
		label_info.configure(text = "Detecting...")

	# Check living here

	# with open("living.txt","w") as f:
	# 	t = str(datetime.datetime.now())
	# 	f.write("Living {}".format(t))
	# 	f.close()
	
	frame_inv = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	photo     = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_inv)) 

	# Show frame in canvas
	my_canvas.create_image(320,30, image = photo, anchor = tk.NW)

	window_detect.after(period,update)

# Main code
update()
window_detect.mainloop()
cap.release()
