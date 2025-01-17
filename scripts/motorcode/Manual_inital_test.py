#!/usr/bin/env python3
import rospy
import RPi.GPIO as GPIO
import time

import enc_states_test as enc_states

## set up variables for stopping motors
##when using the encoder value directly the first will be 0 no matter what
ENC2 = 0
ENC3 = 0
ENC5 = 0
ENC6 = 0

# GPIO pins for PUL, DIR, and SENSOR
PUL_PIN1 = 13
DIR_PIN1 = 11

PUL_PIN2 = 5
DIR_PIN2 = 3

PUL_PIN3 = 24
DIR_PIN3 = 22

PUL_PIN4 = 18
DIR_PIN4 = 16

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUL_PIN1, GPIO.OUT)
GPIO.setup(DIR_PIN1, GPIO.OUT)
GPIO.setup(PUL_PIN2, GPIO.OUT)
GPIO.setup(DIR_PIN2, GPIO.OUT)
GPIO.setup(PUL_PIN3, GPIO.OUT)
GPIO.setup(DIR_PIN3, GPIO.OUT)
GPIO.setup(PUL_PIN4, GPIO.OUT)
GPIO.setup(DIR_PIN4, GPIO.OUT)


# Set initial direction (clockwise)
GPIO.output(DIR_PIN1, GPIO.LOW)
GPIO.output(DIR_PIN2, GPIO.LOW)
GPIO.output(DIR_PIN3, GPIO.LOW)
GPIO.output(DIR_PIN4, GPIO.LOW)

# Function to make one step
def step(rev_per_minute, PUL):

    delay = 60.0 / (400 * 200)
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(delay)  # smallest delay possible
    GPIO.output(PUL, GPIO.LOW)
    time.sleep(delay)  # smallest delay possible

if __name__ == '__main__':
    
    rospy.init_node('man_init', anonymous = True)
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        # Read the sensor value (HIGH or LOW)
        sensor2 = enc_states.enc_status_2()
        sensor3 = enc_states.enc_status_3()
        sensor5 = enc_states.enc_status_5()
        sensor6 = enc_states.enc_status_6()
        
        #motor 1
        if (sensor2 == 1 or ENC2 == 1):
            print("Object detected!")
            # Adjust to desired revolutions per minute
            GPIO.output(PUL_PIN1, GPIO.LOW)
            time.sleep(0.001)
            ENC2 = 1 
        else:
            # Adjust to desired revolutions per minute
            step(50 , PUL_PIN1)
        
        ##motor 2 
        if (sensor3 == 1 or ENC3 == 1):
            print("Object detected!")
            # Adjust to desired revolutions per minute
            GPIO.output(PUL_PIN2, GPIO.LOW)
            time.sleep(0.001)
            ENC3 = 1
        else:
            # Adjust to desired revolutions per minute
            step(50 , PUL_PIN2) 
        
        #motor3
        if (sensor5 == 1 or ENC5 == 1):
            print("Object detected!")
            # Adjust to desired revolutions per minute
            GPIO.output(PUL_PIN3, GPIO.LOW)
            time.sleep(0.001)
            ENC5 = 1
            
        else:
            # Adjust to desired revolutions per minute
            step(50 , PUL_PIN3)
            print("hello world")
        #motor 4
        if (sensor6 == 1 or ENC6 == 1):
            print("Object detected!")
            # Adjust to desired revolutions per minute
            GPIO.output(PUL_PIN4, GPIO.LOW)
            time.sleep(0.001)
            ENC6 = 1
            
        else:
            # Adjust to desired revolutions per minute
            step(50, PUL_PIN4)
        
        if (sensor2 == 1 and sensor3 == 1 and sensor5 ==1 and sensor6 == 1 ):     
            break
        # Add a delay to avoid excessive readings
        time.sleep(0.001)
     
    GPIO.cleanup()        
        


