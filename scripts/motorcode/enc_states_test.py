import RPi.GPIO as GPIO
import time

SENSOR_1 = 29  
SENSOR_2 = 31
SENSOR_3 = 35  
SENSOR_4 = 26
SENSOR_5 = 32
SENSOR_6 = 36

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BOARD)


# Set the sensor pin as input
GPIO.setup(SENSOR_1, GPIO.IN)  
GPIO.setup(SENSOR_2, GPIO.IN)
GPIO.setup(SENSOR_3, GPIO.IN)
GPIO.setup(SENSOR_4, GPIO.IN)
GPIO.setup(SENSOR_5, GPIO.IN)
GPIO.setup(SENSOR_6, GPIO.IN)

def enc_status_1():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor1 = GPIO.input(SENSOR_1)

            if sensor1 == GPIO.HIGH:
                
                # Adjust to desired revolutions per minute
                return 1
            else:
               
                # Adjust to desired revolutions per minute
                
                return 0
            # Add a delay to avoid excessive readings
            time.sleep(0.004)
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt.")
        return "Keyboard interrupt"
        
        
def enc_status_2():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor2 = GPIO.input(SENSOR_2)

            if sensor2 == GPIO.HIGH:
                print("Object detected!")
                # Adjust to desired revolutions per minute
                return 1
            else:
                print("No object detected.")
                # Adjust to desired revolutions per minute
                return 0
            
            time.sleep(0.001)
    except:
        print("\nEncoder not read properly.")
        
def enc_status_3():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor3 = GPIO.input(SENSOR_3)

            if sensor3 == GPIO.HIGH:
                
                # Adjust to desired revolutions per minute
                return 1
            else:
                
                # Adjust to desired revolutions per minute
                return 0
            
            time.sleep(0.001)
    except:
        print("\nEncoder not read properly.")
        
        
def enc_status_4():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor4 = GPIO.input(SENSOR_4)

            if sensor4 == GPIO.HIGH:
                
                # Adjust to desired revolutions per minute
                return 1
            else:
                
                # Adjust to desired revolutions per minute
                return 0
            
            time.sleep(0.001)
    except:
        print("\nEncoder not read properly.")
        
def enc_status_5():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor5 = GPIO.input(SENSOR_5)

            if sensor5 == GPIO.HIGH:
                
                # Adjust to desired revolutions per minute
                return 1
            else:
                
                # Adjust to desired revolutions per minute
                return 0
            
            time.sleep(0.001)
    except:
        print("\nEncoder not read properly.")
        
def enc_status_6():
    try:
        while True:
            # Read the sensor value (HIGH or LOW)
            sensor6 = GPIO.input(SENSOR_6)

            if sensor6 == GPIO.HIGH:
                
                # Adjust to desired revolutions per minute
                return 1
            else:
                
                # Adjust to desired revolutions per minute
                return 0
            
            time.sleep(0.001)            
    except:
        print("\nEncoder not read properly.")
        


# Example usage
if __name__ == "__main__":
    status = get_encoder_status()
    

