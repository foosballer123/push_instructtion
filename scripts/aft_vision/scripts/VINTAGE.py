import cv2
import numpy as np


#img = cv2.imread('C:/Users/benki/Documents/School/Programming/Blue Team/Data/colorful_circles.jpg', 0)
#img = cv2.imread('C:/Users/benki/Documents/School/Programming/Blue Team/Data/stockFoosball.jpg', 0) # Replace with your image path
# cap = cv2.VideoCapture("17output.mp4")
cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


# Set Hough Circle Transform parameters
min_dist = 50  # Minimum distance between detected circles
param1 = 50   # Canny edge detection threshold
param2 = 30   # Acumulator threshold for circle detection
min_radius = 8 # Minimum circle radius
max_radius = 20 # Maximum circle radius

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply median blur to reduce noise
    #gray_frame = cv2.medianBlur(gray_frame, 1)

    # Detect circles
    circles = cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=min_dist,
                               param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)

    if circles is not None:
        # Convert the (x, y) coordinates and radius to integers
        circles = np.uint16(np.around(circles))

        # Draw the detected circle
        # for i in circles[0, :]:
        #     center = (i[0], i[1])
        #     radius = i[2]
        #     cv2.circle(gray_frame, center, radius, (255, 0, 255), 3)

        for i in circles[0]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(gray_frame, center, radius, (255, 0, 255), 3)

        # Show the image with the detected circle
        #cv2.imshow('Detected Circle', gray_frame)
        #cv2.waitKey(25)
        #cv2.destroyAllWindows()

        print(center)
    else:
        print("No circle detected in the image.")

    cv2.imshow('Detected Circle', gray_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
