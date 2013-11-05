#! /usr/bin/env python 
 
# Adapted from http://www.davidhampgonsalves.com/opencv-python-color-tracking/

##########################################################################################
# WebcamColorTrack_MCHE470_Fall2013.py
#
# Script to track red in a webcam image
#
# Requires OpenCV
# 
# Created: 11/2/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
########################################################################################## 
import cv2.cv as cv
from numpy import *  
from time import localtime, strftime
import time
import datetime
 
color_tracker_window = "Tracking Window"

save_data = False

if save_data:
    filename = strftime("%m_%d_%Y_%H%M") #names the output file as the date and time that the program is run
    filepath = filename + ".txt" #gives the path of the file to be opened

class ColorTracker:
    def __init__(self): 
        cv.NamedWindow( color_tracker_window, 1 ) 
        self.capture = cv.CaptureFromCAM(0) 
        
    def run(self): 
        initialTime = time.time() #sets the initial time
        data = zeros((1,3))
        
        while True: 
            img = cv.QueryFrame( self.capture ) 
                        
            #blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 3); 
            
            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) 
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV) 
            
            #limit all pixels that don't match our criteria, in the	is case we are  
            #looking for purple but if you want you can adjust the first value in  
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            #a hue range for the HSV color model 
            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1) 
#             cv.InRangeS(hsv_img, (112, 50, 50), (118, 200, 200), thresholded_img) 

            #try red
            cv.InRangeS(hsv_img, (160, 150, 100), (180, 255, 255), thresholded_img) 
            
            #determine the objects moments and check that the area is large  
            #enough to be our object 
            thresholded_img2 = cv.GetMat(thresholded_img)
            moments = cv.Moments(thresholded_img2,0) 
            area = cv.GetCentralMoment(moments, 0, 0) 
            
            #there can be noise in the video so ignore objects with small areas 
            if(area > 50000): 
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = cv.GetSpatialMoment(moments, 1, 0)/area 
                y = cv.GetSpatialMoment(moments, 0, 1)/area
 
                if save_data:
                    # Save the current time and pixel location into the data array              
                    add = asarray([[time.time() - initialTime,x,y]])
                    data = append(data,add,0)
                
                # convert center location to integers
                x = int(x)
                y = int(y)
                
                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3) 
                
                cv.Circle(overlay, (x, y), 2, (0, 0, 0), 20) 
                cv.Add(img, overlay, img) 
                
                # add the thresholded image back to the img so we can see what was  
                # left after it was applied 
                cv.Merge(thresholded_img2, None, None, None, img) 
             
            #display the image  
            cv.ShowImage(color_tracker_window, img) 
            
            check = cv.WaitKey(1)
            
            if check == 27 or check == 'ESC':
                if save_data:
                    # save the data file as comma separated values
                    data = delete(data, 0, 0) # remove the first row 
                    savetxt(filepath,data,delimiter=",",header = "Time (s), X Position (pixels), Y Position (pixels)")
                break

                
if __name__=="__main__": 
    color_tracker = ColorTracker() 
    color_tracker.run() 
