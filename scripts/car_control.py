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

        '''
        # set up publisher for steering and throttle
        self.servo_steering = rospy.Publisher('/odroid/execution/steering',
                                              Int32, queue_size=10)

        self.servo_throttle = rospy.Publisher('/odroid/execution/throttle',
                                              Int32, queue_size=10)
        '''

        self.controller = vc.ServoController()
        
        # set up subscriber for joystick data
        rospy.Subscriber('/odroid/commands/steering',
                         Int32, self.str_callback)

        rospy.Subscriber('/odroid/commands/throttle',
                         Int32, self.thr_callback)


    def str_callback(self, st):
        steering = st
        #rospy.loginfo("the steering is ", steering)
        #self.servo_steering.publish(steering)
        #controller = vc.ServoController()
        self.controller.setAngle(STEER_SERVO, steering.data)
        #controller.setAngle(0, steering)
        #controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle)

    def thr_callback(self, thr):
        throttle = thr
        #rospy.loginfo("the throttlle is ", throttle)
        print 'throttle is', throttle
        #self.servo_throttle.publish(throttle)
        #controller = vc.ServoController()
        #self.controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2.0*throttle)
        #controller.setAngle(0, steering)
        self.controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle.data)

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
