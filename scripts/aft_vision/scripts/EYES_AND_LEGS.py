import cv2
import numpy as np
import time
import vectorFunctions
import math
import matplotlib
import matplotlib.pyplot as plt
import DEFENSE
import random

from matplotlib.animation import FuncAnimation

# Videocapture uses a camera index as input
cap = cv2.VideoCapture("17output.mp4")

frame_rate = cap.get(cv2.CAP_PROP_FPS)

grid = cv2.imread("C:/Users/benki/Documents/School/Programming/Blue Team/grid.png")

matplotlib.use('TkAgg')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

params = cv2.SimpleBlobDetector_Params()
#... initialize Blob Detection with parameters

start_time = time.time()

x_history = []
y_history = []
time_history = []

#Table pixel bounds
bounds_x = 640
bounds_y = 360

#Player pixel bounds
bounds_x11 = 50
bounds_x12 = 60

bounds_x21 = 470
bounds_x22 = 480

#vector_history = [[],[]]

fig, axs = plt.subplots(1)

# This function is called periodically from FuncAnimation
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
                        ### How do you remove the occassional blob from popping up on the players?

#Creating a Blob Detector based on the version of cv2 installed
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

while True:

    #cv2.waitKey(0)
    # Read a frame from the video stream
    ret, frame = cap.read()  # ret holds the return value of cap.read(). It is True or False based on whether or not there was an image frame to be read. Frame holds the actual image.
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Transfrom the grayscale image to an image with binaray values. An image of bits. THRESH_BINARY is an image type.
    _, thresholded = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    inverted = cv2.bitwise_not(thresholded)

    cv2.imshow("__________", _)
    cv2.imshow("Thresholded", thresholded)

    # The detector uses the native threshold settings set in the parameter function
    keypoints = detector.detect(inverted)

    graph = cv2.addWeighted(frame, 0.90, grid, 0.1, 0)

    # The drawKeypoints function takes an image as input and identifies the regions where keypoints where detected in the image passed to the detect function.
    # In this case, the function is drawing keypoints over the camera inputs in the locations identified in the thresholded image
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Processed Frame", im_with_keypoints)
    cv2.imshow("Graph", graph)

    if (len(keypoints) > 0):

        x = keypoints[0].pt[0]
        y = keypoints[0].pt[1]

        x_history.append(x)
        y_history.append(y)
        time_history.append( time.time() - start_time )

        rod_position = int(random.random()*550)

        print(DEFENSE.defense(y, rod_position))

    # waitKey detects a key pressed for a length of 1 millisecond and 0xFF checks for the specific key being pressed.
    # 0xFF ensures the last 8 bits of the key code are considered. Masking the 'keycode' to 8 bits filters out the unnecissary information from pressed keys (such as ctrl or shift).
    if cv2.waitKey(int(frame_rate)) & 0xFF == ord('q'):
        break

axs.plot(time_history, y_history)
axs.set_xlim([0, time.time() - start_time])

print(len(y_history))
#axs[0].xlim([0, time.time() - start_time])

plt.tight_layout()
plt.show()

cap.release()
cv2.destroyAllWindows()
