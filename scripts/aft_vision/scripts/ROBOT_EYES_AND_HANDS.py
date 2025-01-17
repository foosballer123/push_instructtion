#!/usr/bin/env python3
#ROS IMPLEMENTATION
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

import cv2
import numpy as np
import time
import math
import random

img_received = False

rgb_img = np.zeros((360, 640, 3), dtype = "uint8")

ball_pos = Twist() #geometry position with XYZ for linear and angular

#import matplotlib
#import matplotlib.pyplot as plt
#import DEFENSE

# get the image message
def get_image(ros_img):
	global rgb_img
	global img_received
	# convert to opencv image
	rgb_img = CvBridge().imgmsg_to_cv2(ros_img, "rgb8")
	# raise flag
	img_received = True
	

	
	
		
params = cv2.SimpleBlobDetector_Params()
#... initialize Blob Detection with parameters

start_time = time.time()

x_history = []
y_history = []
time_history = []

#fig, axs = plt.subplots(1)

def set_params(a, b):

    # Change thresholds
    #params.minThreshold = 100;
    #params.maxThreshold = 255;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 3.14159 * 12 * 12 #Ball has radius 10
    params.maxArea = 3.14159 * 14 * 14

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = a
    params.maxCircularity = 1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = b
    params.maxConvexity = 1

    # Filter by Inertia
    params.filterByInertia = False
    #params.minInertiaRatio = 0.01
    #params.maxInertiaRatio = 0.5

set_params(0.4, 0.1)  ### A minimum circularity of 0.2 and a minimum convexity of 0.1 gets rid of most of the noise except for when spinning the characters.
                        
#Creating a Blob Detector based on the version of cv2 installed
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

if __name__ == '__main__':

	rospy.init_node('ROBOT_EYES_AND_HANDS', anonymous = True)
	img_sub = rospy.Subscriber("/camera/color/image_raw", Image, get_image)
	img_pub = rospy.Publisher('/eyes', Image, queue_size = 1)
	
	pos_pub = rospy.Publisher('/ball_pos', Twist, queue_size = 10) 
	
	rate = rospy.Rate(30)
	
	while not rospy.is_shutdown():
	    
		if img_received:
		    #cv2.waitKey(0)
		    # Read a frame from the video stream
			frame = rgb_img
		    
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			_, thresholded = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

			inverted = cv2.bitwise_not(thresholded)

			keypoints = detector.detect(inverted)

			im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
				                           

			#print(im_with_keypoints.shape)
			if (len(keypoints) > 0):

				x = keypoints[0].pt[0]
				y = keypoints[0].pt[1]

				ball_pos.linear.x = x
				ball_pos.linear.y = y
				
				x_history.append(x)
				y_history.append(y)
				time_history.append( time.time() - start_time )

				#rod_position = int(random.random()*550)

				#print(DEFENSE.defense(y, rod_position))
			img_msg = CvBridge().cv2_to_imgmsg(im_with_keypoints, encoding="rgb8")
			img_pub.publish(img_msg)
			pos_pub.publish(ball_pos)
		rate.sleep()
		




	#axs.plot(time_history, y_history)
	#axs.set_xlim([0, time.time() - start_time])

	#print(len(y_history))
	#axs[0].xlim([0, time.time() - start_time])

	#plt.tight_layout()
	#plt.show()

