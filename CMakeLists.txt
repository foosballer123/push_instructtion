cmake_minimum_required(VERSION 3.0.2)
project(aftcode)

## Compile as C++11, supported in ROS Kinetic and newer
# Uncomment this if you want to use C++11
add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  message_runtime
  roscpp
  rospy
  std_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)

# Update find_library to search for the exact library name
find_library(DAQMXBASE_LIB
  NAMES nidaqmxbase.so libnidaqmxbase.so
  PATHS /usr/local/lib /usr/local/natinst/nidaqmxbase/lib64 /usr/local/natinst/nidaqmxbase/lib
  NO_DEFAULT_PATH)

message(STATUS "DAQMXBASE_LIB found: ${DAQMXBASE_LIB}")


if(NOT DAQMXBASE_LIB)
  message(FATAL_ERROR "NI-DAQmxBase library not found. Please check the installation path.")
endif()

## Find pthread library
#find_package(Threads REQUIRED)

################################################
## Declare ROS messages, services, and actions ##
################################################

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate services in the 'srv' folder
# add_service_files(
#   FILES
#   Service1.srv
#   Service2.srv
# )

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
# generate_messages(
#   DEPENDENCIES
#   std_msgs
# )

################################################
## Declare ROS dynamic reconfigure parameters ##
################################################

## To declare and build dynamic reconfigure parameters within this
## package, follow these steps:
## * In the file package.xml:
##   * add a build_depend and a exec_depend tag for "dynamic_reconfigure"
## * In this file (CMakeLists.txt):
##   * add "dynamic_reconfigure" to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * uncomment the "generate_dynamic_reconfigure_options" section below
##     and list every .cfg file to be processed

## Generate dynamic reconfigure parameters in the 'cfg' folder
# generate_dynamic_reconfigure_options(
#   cfg/DynReconf1.cfg
#   cfg/DynReconf2.cfg
# )

###################################
## catkin specific configuration ##
###################################

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES aftcode
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs
  #DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
include_directories(
  ${catkin_INCLUDE_DIRS}
  /usr/local/natinst/nidaqmxbase/include  # Add the correct header directory for NI-DAQmxBase
)

## Declare a C++ executable
#add_executable(cont_rot src/cont_rot.cpp)

## Link executable with the NI-DAQmxBase library, pthread, and Catkin libraries
##target_link_libraries(cont_rot
##  ${catkin_LIBRARIES}  # Link Catkin libraries (roscpp, rospy, std_msgs, etc.)
##  /usr/local/natinst/nidaqmxbase/lib64/libnidaqmxbase.so  # Link to the full path explicitly
  #Threads::Threads     # Link with pthread explicitly
#)

add_executable(testing_connect src/testing_connect.cpp)
target_link_libraries(testing_connect
  ${catkin_LIBRARIES}  # Link Catkin libraries (roscpp, rospy, std_msgs, etc.)
   /usr/lib/x86_64-linux-gnu/libnidaqmx.so
)
#############
## Install ##
#############

## Mark executable scripts (Python etc.) for installation
# catkin_install_python(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark executables for installation
#install(TARGETS cont_rot
 # RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)

#############
## Testing ##
#############

## Add gtest based cpp test target and link libraries
# catkin_add_gtest(${PROJECT_NAME}-test test/test_aftcode.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)

