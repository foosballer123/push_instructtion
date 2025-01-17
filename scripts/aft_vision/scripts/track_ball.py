#!/usr/bin/env python3
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

img_received = False

rgb_img = np.zeros((360, 640, 3), dtype = "uint8")


# get the image message
def get_image(ros_img):
	global rgb_img
	global img_received
	# convert to opencv image
	rgb_img = CvBridge().imgmsg_to_cv2(ros_img, "rgb8")
	# raise flag
	img_received = True

	
if __name__ == '__main__':
	# define the node and subcribers and publishers
	rospy.init_node('track_ball', anonymous = True)
	# define a subscriber to ream images
	img_sub = rospy.Subscriber("/camera/color/image_raw", Image, get_image) 
	# define a publisher to publish images
	img_pub = rospy.Publisher('/tracked_ball', Image, queue_size = 1)
	
	# set the loop frequency
	rate = rospy.Rate(30)

	while not rospy.is_shutdown():
		# make sure we process if the camera has started streaming images
		if img_received:
			# flip the image up			
			#flipped_img = cv2.flip(rgb_img, 0)
			gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
			_, thresholded = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
			inverted = cv2.bitwise_not(thresholded)
			# convert it to ros msg and publish it
			#img_msg = CvBridge().cv2_to_imgmsg(flipped_img, encoding="rgb8")
			img_msg = CvBridge().cv2_to_imgmsg(thresholded, encoding="mono8")
			# publish the image
			img_pub.publish(img_msg)
		# pause until the next iteration			
		rate.sleep()



