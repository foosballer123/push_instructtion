import cv2
import numpy as np
import time
import vectorFunctions
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Videocapture uses a camera index as input
cap = cv2.VideoCapture( 1 )
grid = cv2.imread("C:/Users/benki/Documents/School/Programming/Blue Team/grid.png")

matplotlib.use('TkAgg')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

params = cv2.SimpleBlobDetector_Params()
#... initialize Blob Detection with parameters

vectors = [ [0,0,0], [0,0,0] ] ### tuples holding x, y, and timestamp
velocity = 0
components = [0,0]
forecast_x = 0
forecast_y = 0
start_time = time.time()

forecast_x_history = []
forecast_y_history = []
forecast_time_stamps = []

#Table pixel bounds
bounds_x = 640
bounds_y = 360

#Player pixel bounds
bounds_x11 = 50
bounds_x12 = 60

bounds_x21 = 470
bounds_x22 = 480

#vector_history = [[],[]]

fig, axs = plt.subplots(2)

xs = [0]
ys = [0]

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
        #print("X:", x, "Y:", y)
        # Looking at vector history to determine the natural fluctuation of position while the ball is unmoving
        #vector_history[0].append(x)
        #vector_history[1].append(y)

        # Shifting the vectors so that the recent addition corresponds with the second index
        vectors[0] = vectors[1]
        vectors[1] = [x,y,time.time()]

        ### Divide two vectors by a time stamp to get the velocity
        #print(vectors)


    if ( (vectors[0][2] != 0 ) or (vectors[1][2] != 0) ):
        if ( ( abs( vectors[1][0] - vectors[0][0]) > 0.5 ) or ( abs(vectors[1][1] - vectors[0][1]) > 0.5 ) ):
            velocity, components = vectorFunctions.velocity( vectors[0], vectors[0][2], vectors[1], vectors[1][2])
            plus_x, plus_y = vectorFunctions.forecast(components, ( (bounds_x21 - x) / components[0] ) )
            #print("boundaries", (bounds_x21 - x)/components[0] )

            forecast_x = x + plus_x
            forecast_y = y + plus_y

            forecast_x_history.append(forecast_x)
            forecast_y_history.append(forecast_y)
            forecast_time_stamps.append(time.time())
            print(forecast_x, forecast_y)

            ys.append(velocity)
            xs.append(vectors[1][2])

            #print(ys, xs)
            #print("HAH", y + plus_y) ###Theres problems in the code here. plus_y is way too large a value.
        else:

            ys.append(0)
            xs.append(time.time())
            velocity = 0
            components = [0,0]

            forecast_x = 0
            forecast_y = 0

            forecast_x_history.append(forecast_x)
            forecast_y_history.append(forecast_y)
            forecast_time_stamps.append(time.time())

            #print(ys, xs)

    x_conversion = vectorFunctions.pixels_to_inches(components[0], 0)
    y_conversion = vectorFunctions.pixels_to_inches(components[1], 1)
    v_conversion = math.sqrt( x_conversion**2 + y_conversion**2 )

    # print("Vector", vectors)
    # print("dT", vectors[1][2] - vectors[0][2])
    #print("Velocity and Components", velocity, components )
    # print("Converted Velocity Components: X", x_conversion, "Y: ", y_conversion)
    # print("Converted Velocity Magnitude", v_conversion)
    #print("Forecasted position", forecast_y)



    # waitKey detects a key pressed for a length of 1 millisecond and 0xFF checks for the specific key being pressed.
    # 0xFF ensures the last 8 bits of the key code are considered. Masking the 'keycode' to 8 bits filters out the unnecissary information from pressed keys (such as ctrl or shift).
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.imwrite("test.jpg", frame)
        break


#print("Vector X Range:", max(vector_history[0]) - min(vector_history[0]) )
#print("Vector Y Range:", max(vector_history[1]) - min(vector_history[1]) )

xs = np.array(xs)
xs = xs - start_time
forecast_time_stamps = np.array(forecast_time_stamps)
forecast_time_stamps = forecast_time_stamps - start_time

axs[0].plot(xs, ys)
axs[0].set_xlim([0, time.time() - start_time])

axs[1].plot(forecast_time_stamps, forecast_y_history)
axs[1].set_xlim([0, time.time() - start_time])

#axs[0].xlim([0, time.time() - start_time])

plt.tight_layout()
plt.show()

cap.release()
cv2.destroyAllWindows()


### Question. Does openCV use machine learning algorithms to detect blobs?
### Keypoints.__sizeof__ does not equal 0 when there are no detected blobs. Are the values the dimensionality?
### np.matmul (matrix multiplication)

### NOTES #######################
### The vector positions of the balls fluctuate slightly when the ball is still
### Setting a minimum change in position required before velocity calculations helps fix this

### Should we keep the velocity split into its two components since 'pixels' isnt a standardized unit?

### CURRENT STATE OF CODE ###########
### The code can calculate velocity and split it into its individual components
### The code can convert the individual pixel components of velocity to their counterpart in inches
### The next step should be forecasting future positions of the ball
### 
### The ball still skips detection periodically. It could be due to lighting conditions or contact with the white regions on the board. The image filtering still needs to be messed with.
###
### FORECASTING
### Predict the time it would take a the ball to reach a select point in the board using its current velocity
### There are TWO REGIONS on the board that can interact with the ball. Each can be represented by a range of pixel values.
### Each player gaurds a specific matrix of pixels.
### Each matrix of pixels contains a number of points
### The future position of the ball will land in one of the matrices
### Given the balls velocity, we can calculate its trajectory vector within the bounds of the board
### The trajectory vector will land within the bounds of one of the player matrices
### Its less a matter of how to predict the future position of the ball but what is the most efficient method that will least infringe on the run time of the code
###
### break the video into frames to slow down the process of forecasting, hopefully making the problems with the code more obvious.

### GRAPH THE LIVE VELOCITY OF THE BALL (using ROS? or matplotlib)
### Am I using noising data that is getting amplified in the calculation process?
### small errors in the delta t will be amplified because of the low refresh rate of the camera
### Try collecting 10 sample data points at once for velocity measurements ( 1 measurement

### PROBLEMS FOR NEXT SESH ###
### Discover the pixel values associated with each point on the board
### Discover the positive and negative directions on the board
### Break down the forecasting process into individual frames (maybe try an image approach instead of using a live video feed)
### (Try to get chopsticks from panda express for holding the ball)
###
### You should never be getting a negative value from forecasting because the board only has POSITIVE COORDINATES

############################################################################################################
### This project is the perfect example for how difficult it is to understand and manipulate the real
### The amount of knowledge and experience required to do a simple task independetly of human interaction is monstrous compared to the task itself
### All of what we are trying to do is a cheap imitation of the beautiful mecahnisms of nature

### This project is also an interesting example of how man has slowly abstracted himself away from nature
### Soccer was once a game people only ever thought to play on a field.
### Then somebody thought to abstract it to a simplified game played between two people.
### Now we're taking it to the next level: removing the human entirely.
############################################################################################################
