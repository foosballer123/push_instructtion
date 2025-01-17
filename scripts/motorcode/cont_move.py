import RPi.GPIO as GPIO
import time

# GPIO pins for PUL and DIR
PUL_PIN = 5
DIR_PIN = 3

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Set initial direction (clockwise)
GPIO.output(DIR_PIN, GPIO.LOW)

# Function to make one step
def step():
    GPIO.output(PUL_PIN, GPIO.HIGH)
    time.sleep(0.0005)  # smallest delay possible
    GPIO.output(PUL_PIN, GPIO.LOW)
    time.sleep(0.0005)  # smallest delay possible

# Function to make continuous revolutions
def continuous_rotation(rev_per_minute):
    delay = 60.0 / (400 * rev_per_minute)  # 400 steps per revolution
    for x in range(400): # does one full revolution 
        step()


try:
    continuous_rotation(100)  # Adjust to desired revolutions per minute
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

