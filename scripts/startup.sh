#!/bin/bash
source /opt/ros/noetic/setup.bash
source /home/aft2024/catkin_ws/devel/setup.bash


# start ui
roslaunch realsense2_camera rs_camera.launch color_width:=640 color_height:=360 color_fps:=30 format:=rgb8 &
sleep 5

python3 ~/catkin_ws/src/aftcode/scripts/aft_vision/scripts/HOUGH_TRANSFORM.py &

sleep 5

#rosrun aftcode motor1.py &
#sleep 3

#rosrun aftcode motor2.py &
#sleep 3

rosrun aftcode motor3.py &
sleep 3

rosrun aftcode motor4.py &
sleep 3

wait


