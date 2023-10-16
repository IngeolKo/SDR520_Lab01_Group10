#!/usr/bin/env python

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import rospy
import math


class Rotator():

    def __init__(self):
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    def rotate_forever(self):
        self.twist = Twist()

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.twist.angular.z = 0.1
            self._cmd_pub.publish(self.twist)
            rospy.loginfo('Rotating robot: %s', self.twist)
            r.sleep()

class Move():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        rospy.Subscriber("/odom", Odometry, self.odom_callback)

        self.robot_x = 0.0
        self.robot_y = 0.0

    def odom_callback(self, odom_msg):
        # Extract the x and y position from the Odometry message
        self.robot_x = odom_msg.pose.pose.position.x
        self.robot_y = odom_msg.pose.pose.position.y

    def get_position(self):
        # Return the current x and y position of the robot
        return self.robot_x, self.robot_y

    def move(self, x, y):
        self.twist = Twist()

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.twist.linear.x = x
            self.twist.linear.y = y
            self.twist.angular.z = 0
            self._cmd_pub.publish(self.twist)
            rospy.loginfo('Moving robot...')
            r.sleep()
    
    def moveTo(self, x, y):
        self.twist = Twist()
        
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            if abs(self.robot_x - x) < 0.01 and abs(self.robot_y - y) < 0.01:
                rospy.loginfo('Reached the target position')
                self.twist.linear.x = 0
                self.twist.linear.y = 0
                self._cmd_pub.publish(self.twist)
                break
            # move in the x direction
            if self.robot_x < x:
                self.twist.linear.x = 0.2
            else:
                self.twist.linear.x = 0  

            # move in the y direction
            if self.robot_y < y:
                self.twist.linear.y = 0.2
            else:
                self.twist.linear.y = 0

            self._cmd_pub.publish(self.twist)
            rospy.loginfo('X pos: %f, Y pos: %f', self.robot_x, self.robot_y)

            r.sleep()

        

def main():
    rospy.init_node('move to target')
    try:
        move = Move()
        move.moveTo(1, 1)
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()



