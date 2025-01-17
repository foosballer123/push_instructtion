import cv2
import numpy as np

# Videocapture uses a camera index as input
cap = cv2.VideoCapture(1)

# fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# writer = cv2.VideoWriter('output.avi', fourcc, 30.0, (1280, 720))

params = cv2.SimpleBlobDetector_Params()
#... initialize Blob Detection with parameters


# Change thresholds
params.minThreshold = 100;
params.maxThreshold = 255;

# Filter by Area.
params.filterByArea = True
params.minArea = 3.14159 * 2 * 2
params.maxArea = 3.14159 * 50 * 50

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.5
params.maxCircularity = 1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.8
# params.maxConvexity = 1

# Filter by Inertia
params.filterByInertia = False
# params.minInertiaRatio = 0.01


#Creating a Blob Detector based on the version of cv2 installed
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read() # ret holds the return value of cap.read(). It is True or False based on whether or not there was an image frame to be read. Frame holds the actual image.
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Transfrom the grayscale image to an image with binaray values. An image of bits. THRESH_BINARY is an image type.
    _, thresholded = cv2.threshold(gray, 50 ,255, cv2.THRESH_BINARY)

    cv2.imshow("__________", _)
    cv2.imshow("Thresholded", thresholded)

    # The detector uses the native threshold settings set in the parameter function
    keypoints = detector.detect(thresholded)

    # The drawKeypoints function takes an image as input and identifies the regions where keypoints where detected in the image passed to the detect function.
    # In this case, the function is drawing keypoints over the camera inputs in the locations identified in the thresholded image
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Processed Frame", im_with_keypoints)

    if ( len(keypoints) > 0):
        x = keypoints[0].pt[0]
        y = keypoints[0].pt[1]
        print(x, y)

    # waitKey detects a key pressed for a length of 1 millisecond and 0xFF checks for the specific key being pressed.
    # 0xFF ensures the last 8 bits of the key code are considered. Masking the 'keycode' to 8 bits filters out the unnecissary information from pressed keys (such as ctrl or shift).
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()


### Question. Does openCV use machine learning algorithms to detect blobs?
### Keypoints.__sizeof__ does not equal 0 when there are no detected blobs. Are the values the dimensionality?
### np.matmul (matrix multiplication)


### How can you average all of the points inside of the keypoints function
