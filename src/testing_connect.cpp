#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <NIDAQmx.h>

#define DIRECTION_CHANNEL "Dev1/port0/line1"  // Digital output channel for direction (P0.0)
#define PULSE_CHANNEL "Dev1/port0/line0"      // Digital output channel for pulse (P0.1)

// Function to set up the digital output channels for motor control
void setupMotorControl(TaskHandle &taskHandle)
{    
    // Create a task for motor control
    DAQmxCreateTask("", &taskHandle);

    // Create digital output channels for direction and pulse
    DAQmxCreateDOChan(taskHandle, DIRECTION_CHANNEL, "", DAQmx_Val_ChanForAllLines);
    DAQmxCreateDOChan(taskHandle, PULSE_CHANNEL, "", DAQmx_Val_ChanForAllLines);
    
    // Start the task
    DAQmxStartTask(taskHandle);
}

// Function to control motor direction and pulse
void controlMotor(TaskHandle taskHandle, bool direction, int pulseCount, double pulseFrequency)
{
    // Set the direction (1 for forward, 0 for backward)
    uInt8 directionData = direction ? 1 : 0;
    int32 samp_p_channel = 1;
    DAQmxWriteDigitalLines(taskHandle, 1, true, 10.0, DAQmx_Val_GroupByChannel, &directionData, &samp_p_channel, NULL);

    // Calculate pulse duration based on the desired frequency
    double pulseDuration = 1.0 / pulseFrequency; // Pulse period in seconds
    uInt8 pulseData = 1;

    for (int i = 0; i < pulseCount; ++i)
    {
        // Pulse high
        DAQmxWriteDigitalLines(taskHandle, 1, true, 10.0, DAQmx_Val_GroupByChannel, &pulseData, &samp_p_channel, NULL);

        // Wait for half of the period
        usleep(pulseDuration * 500000);  // Convert to microseconds

        // Pulse low
        pulseData = 0;
        DAQmxWriteDigitalLines(taskHandle, 1, true, 10.0, DAQmx_Val_GroupByChannel, &pulseData, &samp_p_channel, NULL);
        // Wait for the other half of the period
        usleep(pulseDuration * 500000);  // Convert to microseconds
    }
}


int main(int argc, char** argv)
{
    ros::init(argc, argv, "nema_motor_control_node");
    ros::NodeHandle nh;

    // ROS Publisher to send data (optional, can be used to monitor motor status)
    ros::Publisher pub = nh.advertise<std_msgs::Float64>("motor_status", 10);
    
    // Setup motor control
    TaskHandle taskHandle = 0;
    setupMotorControl(taskHandle);
    
    ros::Rate loop_rate(10);  // Loop at 10 Hz

    bool direction = true;  // Motor direction (true = forward, false = reverse)
    int pulseCount = 200;   // Number of pulses to generate per loop iteration
    double pulseFrequency = 60.0; // Pulse frequency in Hz (motor speed)



    while (ros::ok())
    {
        // Control the motor by sending pulses
        controlMotor(taskHandle, direction, pulseCount, pulseFrequency);

        // Optional: Publish a message about motor status
        std_msgs::Float64 msg;
        msg.data = pulseFrequency;  // Send the motor pulse frequency as status
        pub.publish(msg);

        // Toggle direction every cycle (optional)
        direction = !direction;  // Reverse direction after each loop iteration

        ros::spinOnce();
        loop_rate.sleep();
    }

    // Cleanup and stop the task before exiting
    DAQmxStopTask(taskHandle);
    DAQmxClearTask(taskHandle);

    return 0;
}

