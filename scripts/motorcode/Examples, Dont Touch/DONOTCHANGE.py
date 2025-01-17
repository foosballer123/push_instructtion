import RPi.GPIO as GPIO
import time

# GPIO pins for PUL, DIR, and SENSOR
PUL_PIN = 40
DIR_PIN = 38
SENSOR_PIN = 37  # Adjust this based on your wiring

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Set the sensor pin as input



try:
    while True:
        # Read the sensor value (HIGH or LOW)
        sensor_value = GPIO.input(SENSOR_PIN)

        if sensor_value == GPIO.HIGH:
            print("Object detected!")
            # Adjust to desired revolutions per minute
            break
        else:
            print("No object detected.")
            # Adjust to desired revolutions per minute
            time.sleep(0.004) 

        # Add a delay to avoid excessive readings
        #time.sleep(0.001)

except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt.")
finally:
    GPIO.cleanup()
