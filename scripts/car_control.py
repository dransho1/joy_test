#!/usr/bin/env python

import roslib; roslib.load_manifest('joy_test')
import rospy
import servotest as vc
import serial

from std_msgs.msg import Float64, Int64, Int32, String

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
        
        # set up subscriber for joystick data
        rospy.Subscriber('/odroid/commands/steering',
                         Int32, self.str_callback)

        rospy.Subscriber('/odroid/commands/throttle',
                         Int32, self.thr_callback)


    def str_callback(self, st):
        steering = st
        #rospy.loginfo("the steering is ", steering)
        self.controller.setAngle(STEER_SERVO, steering.data)
        #controller.setAngle(0, steering)

    def thr_callback(self, thr):
        throttle = thr
        #rospy.loginfo("the throttlle is ", throttle)
        self.controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + throttle.data)

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
