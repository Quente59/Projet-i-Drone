#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x
x = 0



def talker():

    global x
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/turtle1/pose', Pose, callback)
    
    while not rospy.is_shutdown():
        

	if x < 10.0 :
            message = Twist()
	    message.linear.x = 2.0
	    message.angular.z = 0.0
            #rospy.loginfo(message)
            pub.publish(message)
            rate.sleep()

        else :
            message = Twist()
	    message.linear.x = 0.0
	    message.angular.z = 5.0
            #rospy.loginfo(message)
            pub.publish(message)
            rate.sleep()


def callback(position):
    global x
    
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position)
    x = position.x
    



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
