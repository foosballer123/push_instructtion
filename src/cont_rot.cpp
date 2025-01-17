#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <NIDAQmx.h>

#define CHANNEL "Dev1/ai0"  // Analog input channel for the NI USB-6009

// Change the return type to double
double setupNIUSB6009()
{
    // Initialize the DAQmx task
    TaskHandle taskHandle = 0;
    DAQmxCreateTask("", &taskHandle);
    DAQmxCreateAIVoltageChan(taskHandle, CHANNEL, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, NULL);
    DAQmxStartTask(taskHandle);

    // Declare the buffer to store the analog input
    float64 data[1];

    // Read the analog input
    DAQmxReadAnalogF64(taskHandle, 1, 10.0, DAQmx_Val_GroupByChannel, data, 1, NULL, NULL);

    // Stop and clear the task
    DAQmxStopTask(taskHandle);
    DAQmxClearTask(taskHandle);

    // Return the acquired data
    return data[0];  // Now return the data as a double
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "ni_usb_6009_node");
    ros::NodeHandle nh;

    // ROS Publisher to send data
    ros::Publisher pub = nh.advertise<std_msgs::Float64>("sensor_data", 10);
    
    ros::Rate loop_rate(10);  // Loop at 10 Hz

    while (ros::ok())
    {
        // Now `setupNIUSB6009` returns a double
        double sensor_data = setupNIUSB6009();

        // Create and publish a message
        std_msgs::Float64 msg;
        msg.data = sensor_data;
        pub.publish(msg);

        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}

