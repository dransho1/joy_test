#!/usr/bin/env python

import roslib; roslib.load_manifest('joy_test')
import rospy
import servotest as vc
import serial

from std_msgs.msg import Float64, Int32, Int32MultiArray
from joy_test.msg import IntList

# global variables
MOTOR_NEUTRAL = 1500
ESC_SERVO = 1
STEER_SERVO = 0


# our controller class
class Controller:

    # called when an object of type Controller is created
    def __init__(self):

        # initialize rospy
        rospy.init_node('car_controller')

        # create controller
        self.controller = vc.ServoController()

        rospy.Subscriber('odroid/commands/combined',
                         IntList, self.motor_callback)

    def motor_callback(self, code):
        button = code.button
        steering = code.steer
        throttle = code.thr
        if button==1:
            print "killswitch engaged shutting down script, button is:", button
            self.controller.setAngle(STEER_SERVO, 90)
            self.controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL
                                        + 0*throttle)
            rospy.signal_shutdown("Killswitch")
        else:
            print button
            self.controller.setAngle(STEER_SERVO, steering)
            self.controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle)
        
        
    def run(self):
        rospy.spin()

    # okay great, now we can send data from one node to another. 
    # want to now use that data to set the angle of the car
    # and integrate this with the car's project_server.py script

# main function
if __name__ == '__main__':
    try:
        ctrl = Controller()
        ctrl.run()
    except rospy.ROSInterruptException:
        pass
