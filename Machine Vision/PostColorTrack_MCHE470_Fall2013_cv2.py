#! /usr/bin/env python 
 
 
##########################################################################################
# PostColorTrack_MCHE470_Fall2013_cv2.py
#
# Script to process Mini-Project 3b videos
#
# Requires OpenCV
# 
# Created: 11/2/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 11/4/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - hard coded video names due to Tkinter file dialog bug
#
########################################################################################## 
 
import cv2 as cv2
import numpy as np
from time import localtime, strftime, sleep
from Tkinter import Tk
from tkFileDialog import askopenfilename
from matplotlib.pyplot import * # Grab MATLAB plotting functions
 
color_tracker_window = "Color Tracker"

filename = strftime("%m_%d_%Y_%H%M%S") #names the output file as the date and time that the program is run
filepath = filename + ".txt" #gives the path of the file to be opened
    
f = open(filepath, "a+") #opens the output file in append mode
f.write('Time (s), X Position (pixels), Y Position (pixels)' + '\n') 

show_images = 1
print_images = 0

class ColorTracker:
    def __init__(self): 
#         cv2.NamedWindow( color_tracker_window, 1 ) 

#         tk = Tk()
#         tk.withdraw() # we don't want a full GUI, so keep the root window from appearing
#         video_filename = askopenfilename(parent=tk) # show an "Open" dialog box and return the path to the selected file
#         
#         tk.destroy()
        
#         video_filename = '/Users/josh/Desktop/Videos for Lecture/Movie on 11-4-13 at 7.12 PM.mov'
#         video_filename = '/Users/josh/Desktop/Videos for Lecture/Movie on 11-4-13 at 7.18 PM.mov'
#         video_filename = '/Users/josh/Desktop/Videos for Lecture/Movie on 11-4-13 at 7.56 PM.mov'
#         video_filename = '/Users/josh/Desktop/Videos for Lecture/Movie on 11-4-13 at 7.59 PM.mov'
          
        self.capture = cv2.VideoCapture(video_filename)
        
        
    def run(self): 
        initialTime = 0. #sets the initial time
#         num_Frames = int(  cv2.GetCaptureProperty( self.capture, cv2.CV_CAP_PROP_FRAME_COUNT ) )
        num_Frames = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        fps = self.capture.get(cv2.cv.CV_CAP_PROP_FPS)
#         fps = cv2.GetCaptureProperty( self.capture, cv2.CV_CAP_PROP_FPS )
        
        for ii in range(num_Frames-9):
        
            print('Frame: ' + str(ii) + ' of ' + str(num_Frames))
            # read the ii-th frame
#             img = cv2.QueryFrame( self.capture )  
            img = self.capture.read()[1]
            
            if show_images:
                cv2.imshow('Raw Frame',img)
                raw_input("Press Enter to continue...")
                
                if print_images:
                    savefig('Raw_Frame.png')
                        
            
            # Blur the source image to reduce color noise 
            # cv2.Smooth(img, img, cv2.CV_BLUR, 10) 
            img = cv2.blur(img,(10,10))
            
            if show_images:
                cv2.imshow('Blurred',img)
                raw_input("Press Enter to continue...")
                
                if print_images:
                    savefig('10x10_blur.png')

            
            # Convert the image to hsv(Hue, Saturation, Value) so its  
            # It's easier to determine the color to track(hue) 
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

            # Define min and max HSV values to threshold
            Track_MIN = np.array([0, 0, 245],np.uint8)
            Track_MAX = np.array([180, 10, 255],np.uint8)
            
            # threshold the image
            thresholded_img = cv2.inRange(hsv_img, Track_MIN, Track_MAX)
            
            if show_images:
                cv2.imshow('Thresholded Image',thresholded_img)
                raw_input("Press Enter to continue...")
                
                if print_images:
                    savefig('Thresholded_Frame.png')
            
            # fill the top with black
            thresholded_img[0:75,0:720] = 0
            thresholded_img[0:480,650:720] = 0
            
            if show_images:
#             if ii > 100:
                cv2.imshow('Thresholded Image',thresholded_img)
                raw_input("Press Enter to continue...")
            
            
            #determine the objects moments and check that the area is large  
            #enough to be our object 
#             thresholded_img2 = cv2.GetMat(thresholded_img)
            moments = cv2.moments(thresholded_img,0) 
            area = moments['m00'] 
            
            
            # there can be noise in the video so ignore objects with small areas 
            if(area > 1500): 
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = moments['m10'] / area
                y = moments['m01'] / area

                elapsedTime = ii/fps
            
                f.write(str(elapsedTime) + ',' + '%013.9f' % x + ',' + '%013.9f' % y + "\n") #prints output to the specified output file for later use
                
                x = int(x)
                y = int(y)
                
#                 #create an overlay to mark the center of the tracked object 
#                 overlay = cv2.CreateImage(cv2.GetSize(img), 8, 3) 
#                 
#                 cv2.Circle(overlay, (x, y), 2, (255, 255, 255), 20) 
#                 cv2.Add(img, overlay, img) 
#                 #add the thresholded image back to the img so we can see what was  
#                 #left after it was applied 
#                 cv2.Merge(thresholded_img, None, None, None, img) 
#              
#             #display the image  
#             cv2.ShowImage(color_tracker_window, img) 
            
        # close the data file
        f.close()

                
if __name__=="__main__": 
    color_tracker = ColorTracker() 
    color_tracker.run() 
