#!/usr/bin/env python


import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x = 0
global x

def callback(position):

    global x
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position)

    x = position.x

def motor():
    global x
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('motor', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/turtle1/pose', Pose, callback)
    

    while not rospy.is_shutdown():
	message = Twist()

        

	if x < 10:

            message.linear.x = 2.0
	    pub.publish(message)
            rate.sleep()

	else:
            
	    message.linear.x = 0.0
	    message.angular.z = 5.0
            pub.publish(message)
            rate.sleep()

	
        
    

if __name__ == '__main__':
    try:
        motor()
    except rospy.ROSInterruptException:
        pass
