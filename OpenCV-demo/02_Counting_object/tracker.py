#Import necessary packages
from scipy.spatial import distance as dist 
from collections import OrderedDict
import numpy as np 
import math

class CentroidTracker():

    #Create variable for this class to store
    def __init__(self,maxDisappeared = 50):
        # We need 4 parameter
        # nextObjectID give object in frame a id
        self.nextObjectID = 0
        # Create Odered Dict for store object's id and objects possition
        self.objects = OrderedDict()
        # Create a Odered Dict for store object's id and consecutive frame appeared of this object,
        #if larger than 50 then remove this object ID
        self.disappeared = OrderedDict()
        # Define maximum frame consecutive allow object with this id disappeared
        self.maxDisappeared = maxDisappeared

    # Create a register method for add new object'id
    def register(self, centroid):
        # Store object position with the key is object's ID
        #  centroid similar is (x,y), store it in objects dict
        self.objects[self.nextObjectID] = centroid
        #  with this object's id, create a zero value maxDisappeared corresponded, store it in maxDisappeared dict
        self.disappeared[self.nextObjectID] = 0
        # Increase your ID when you add register
        self.nextObjectID += 1
    
    #Create a deregister for deleted dissapeared object
    def deregister(self, objectID):
        # delete objects postion dict and disappeared dict
        del self.objects[objectID]
        del self.disappeared[objectID]

    #Create a update function, update consecutive frame if we dont see any frames
    # The format of  list rects is similar (x,y,x_end,y_end)
    def update(self, rects):

        # if there's no any rects in list
        if len(rects) == 0: 
            # increade  the dissapeared value in disappeared list
            #Loop over each ID in dict
            for objectID in list(self.disappeared.keys()):
                
                #increade value 1 frame disappeared
                self.disappeared[objectID] +=1

                #if we reach maximum number of maxdisappeared then del this id out of our frame

                if self.disappeared[objectID] > self.maxDisappeared:
                    #Delete this using deregister method
                    self.deregister(objectID)

                    # retrun early as there is no bbox 
                    return self.objects 
        # Else meaning there are somthing in rects list
        # inititalize an array of input centroids for the current frame, in the begin every position will be zeros

        inputCentroids = np.zeros((len(rects),2),dtype = "int")
        # loop over the bounding box rectangles
        for (i,(startX,startY,endX,endY)) in enumerate(rects):
            #Calculate the centroid
            cX = int((startX + endX)/2.0) # divice 2 will return int
            cY = int((startY + endY)/2.0)
            #Set value in inputCentroids list corresponded  this indicated 
            inputCentroids[i] = (cX,cY)

        # IF there is no objects we are tracking, we'll register each of the new objects for objects dict and disappeared list
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                #Updated (x,y) for each id
                self.register(inputCentroids[i])
        
        #Else if there is have some thing in objects dict then we have to match the input for centroids
        #existed by eclidean distance menthod
        else:
            # Take id list in objects dict
            objectIDs = list(self.objects.keys())
            # Take the position of centroid corresponding each objectIDs list
            objectCentroids = list(self.objects.values())
            # compute the distance between each pair of object
			# centroids and input centroids, respectively -- our
			# goal will be to match an input centroid to an existing
			# object centroid
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            # in order to perform this matching we must (1) find the
			# smallest value in each row and then (2) sort the row
			# indexes based on their minimum values so that the row
			# with the smallest value is at the *front* of the index
			# list
            rows = D.min(axis=1).argsort()
            # next, we perform a similar process on the columns by
			# finding the smallest value in each column and then
			# sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]
            usedRows = set() # Set just like a dict but contain unique val
            usedCols = set()

            # loop over the combination of (row, column) index tuple

            for (row,col) in zip(rows,cols):
                #if we have already examined either the row or column value before, ignore it
                if row in usedRows or col in usedCols:
                    continue

                # otherwise, grab the object ID for current row, set its new centroid, and 
                # reset the disappeared counter
                objectID = objectIDs[row]
                #Update it
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0

                # indicate that we have examined each of the row and column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)
            
            # compute both the row and column index we have NOT yet examined
            unusedRows = set(range(0,D.shape[0])).difference(usedRows)
            unusedCols = set(range(0,D.shape[1])).difference(usedCols)

            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    # grab the object ID for the corresponding row
                    # index and increment the disappeared counter
                    objectID = objectIDs[row]
                    self.disappeared[objectID] +=1

                    # check to see if the number of consecutive
                    # frames the object has been marked "disappeared"
                    # for warrants deregistering the object
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
            # otherwise, if the number of input centroids is greater
            # than the number of existing object centroids we need to
            # register each new input centroid as a trackable object

            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        return self.objects
                


class EuclideanDistTracker:
    def __init__(self):
        #Print out 1 time
        print("Init only run once time")
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids