#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import random
import math

 
turtle1_pose = Pose()
turtle2_pose = Pose()

 
def turtle1_callback(msg):
    global turtle1_pose
    turtle1_pose = msg

 
def turtle2_callback(msg):
    global turtle2_pose
    turtle2_pose = msg
 
def move_turtle1_randomly(pub):
    twist = Twist()
    twist.linear.x = random.uniform(0.5, 2.0)   
    twist.angular.z = random.uniform(-2.0, 2.0)   
    pub.publish(twist)

 
def chase_turtle():
    rospy.init_node('turtle_chaser', anonymous=True)

 
    rospy.Subscriber('/turtle1/pose', Pose, turtle1_callback)
    rospy.Subscriber('/turtle2/pose', Pose, turtle2_callback)

    
    turtle1_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    turtle2_pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
         
        move_turtle1_randomly(turtle1_pub)
        
     
        distance = math.sqrt((turtle1_pose.x - turtle2_pose.x)**2 + (turtle1_pose.y - turtle2_pose.y)**2)
        angle_to_turtle1 = math.atan2(turtle1_pose.y - turtle2_pose.y, turtle1_pose.x - turtle2_pose.x)
        angle_diff = angle_to_turtle1 - turtle2_pose.theta

        
        twist = Twist()
        twist.linear.x = min(2.0 * distance, 2.0) 
        twist.angular.z = 4.0 * angle_diff
        turtle2_pub.publish(twist)

        rate.sleep()

if __name__ == '__main__':
    try:
        chase_turtle()
    except rospy.ROSInterruptException:
        pass
