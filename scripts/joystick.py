#!/usr/bin/env python

# Boilerplate initialization stuff -- make sure to load the manifest
# from this package in order to be able to parse all of the correct
# messages. 

import roslib; roslib.load_manifest('joy_test')
import rospy
import mc
import pygame
import time

# make a message class for reporting
from std_msgs.msg import Float64, Int32, String

#from blobfinder.msg import MultiBlobInfo

######################################################################
# Define a class to implement our node. This gets instantiated once
# when the node is run (see very bottom of file)

def joystick():
    # Publish joystick messages to a topic
    joystick_steering = rospy.Publisher('/odroid/commands/steering',
                                        Int32, queue_size=10)
    joystick_throttle = rospy.Publisher('/odroid/commands/throttle',
                                        Int32, queue_size=10)
    # use float 64 as a message passing
    rospy.init_node('joystick')

    #################################################################
    # Main loop of program
    controller = mc.hci_init()

    while not rospy.is_shutdown():
        
        steering, throttle = mc.hci_input(controller)
        steering = int(-1*steering*90 + 90)
        throttle = int(-1*90*throttle)
        #rospy.loginfo('steering is ', steering)
        #rospy.loginfo('throttle is ', throttle)
        #code = steering+throttle
        joystick_steering.publish(steering)
        joystick_throttle.publish(throttle)
        rospy.sleep(0.01) # sleep for 1/100 sec
        


if __name__ == '__main__':

    try:
        #rospy.spin()
        joystick()
    except rospy.ROSInterruptException:
        pass
