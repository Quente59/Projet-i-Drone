#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x
global y
global z
x = 0
y = 0
z = 0



def talker_follower():

    global x
    global y
    global z
    
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/turtle1/pose', Pose, callback)
    
    while not rospy.is_shutdown():
        message = Twist()
        message.linear.x = x
        message.linear.y = y
        message.linear.z = z
        #rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()



def callback(position):
    global x
    global y
    global z
    
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position)
    x = position.x
    y = position.y
    z = position.z
    



if __name__ == '__main__':
    try:
        talker_follower()
    except rospy.ROSInterruptException:
        pass
