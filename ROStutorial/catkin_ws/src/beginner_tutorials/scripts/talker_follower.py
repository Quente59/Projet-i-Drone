#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x
global y
global z

global x2
global y2
global z2
    
x = 0
y = 0
z = 0

x2 = 0
y2 = 0
z2 = 0



def talker_follower():

    global x
    global y
    global z
    
    global x2
    global y2
    global z2
   
    
    pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rospy.Subscriber('/turtle2/pose', Pose, callback2)
    
    while not rospy.is_shutdown():
       
        message2 = Twist()
        
        if x > x2 : 
            
            message2.linear.x = 1.0
	    
        
        else:
            message2.linear.x = 0.0
            message2.angular.z = -5.0

        """if y > y2 : 
            
            message2.linear.y = 1.0
            
        else:
            message2.linear.y = -1.0"""
        
        """if z > z2 : 
            
            message2.angular.z = 5.0
            
        else:
            message2.angular.z = -5.0"""
        
   
        
        #rospy.loginfo(message2)

        pub2.publish(message2)
        rate.sleep()



def callback(position):
    global x
    global y
    global z
    
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position)
    x = position.x
    y = position.y
    z = position.theta
    
def callback2(position2):
    global x2
    global y2
    global z2
    
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position2)
    
    x2 = position2.x
    y2 = position2.y
    z2 = position2.theta
    



if __name__ == '__main__':
    try:
        talker_follower()
    except rospy.ROSInterruptException:
        pass
