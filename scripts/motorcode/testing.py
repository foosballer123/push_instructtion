import RPi.GPIO as GPIO
import time

# GPIO pins for PUL, DIR, and SENSOR
PUL_PIN = 5
DIR_PIN = 3
SENSOR_PIN = 37 # Adjust this based on your wiring

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Set the sensor pin as input

# Set initial direction (clockwise)
GPIO.output(DIR_PIN, GPIO.HIGH)

# Function to make one step
def step(rev_per_minute):
    delay = 60.0 / (400 * rev_per_minute)
    GPIO.output(PUL_PIN, GPIO.HIGH)
    time.sleep(delay)  # smallest delay possible
    GPIO.output(PUL_PIN, GPIO.LOW)
    time.sleep(delay)  # smallest delay possible



try:
    while True:
        # Read the sensor value (HIGH or LOW)
        sensor_value = GPIO.input(SENSOR_PIN)

        if sensor_value == GPIO.HIGH:
            print("Object detected!")
            # Adjust to desired revolutions per minute
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(0.001)
            break
        else:
            print("No object detected.")
            # Adjust to desired revolutions per minute
            step(50) 

        # Add a delay to avoid excessive readings
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt.")
finally:
    GPIO.cleanup()
