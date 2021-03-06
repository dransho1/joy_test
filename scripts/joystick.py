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
from std_msgs.msg import Float64, Int32, Int32MultiArray
from joy_test.msg import IntList

#from blobfinder.msg import MultiBlobInfo

######################################################################

def joystick():
    # Publish joystick messages to a topic

    joystick_combined = rospy.Publisher('odroid/commands/combined',
                                        IntList,
                                        queue_size=12)
    
    # use float 64 as a message passing
    rospy.init_node('joystick')

    #################################################################
    # Main loop of program
    controller = mc.hci_init()
    a = IntList()
    while not rospy.is_shutdown():
        steering, throttle = mc.hci_input(controller)
        steering = int(-1*steering*90 + 90)
        throttle = int(-1*90*throttle)
        button = mc.hci_button(controller)    # killswitch is B

        # write to publisher
        a.steer = steering
        a.thr = throttle
        a.button = button
        joystick_combined.publish(a)
        rospy.sleep(0.01) # sleep for 1/100 sec
        


if __name__ == '__main__':

    try:
        #rospy.spin()
        joystick()
    except rospy.ROSInterruptException:
        pass
