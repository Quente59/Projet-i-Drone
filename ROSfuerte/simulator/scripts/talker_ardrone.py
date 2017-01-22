#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msg.msg import Empty
from tum_simulator.msg import Altimeter

global z
z = 0



def talker_ardrone():

    global z
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=10)
    pub_land = rospy.Publisher('/ardrone/land', Empty, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/altimeter', Altimeter, callback)
    
    decoller = True
    
    while not rospy.is_shutdown():
    
    if decoller :
        message = Empty()
        message = ''
        #rospy.loginfo(message)
        pub_takeoff.publish(message)
        decoller = False
        
	if z == 20.0 :
        message = Twist()
        message.linear.x = 0.0
        message.linear.y = 0.0
        message.linear.z = 0.0
        message.angular.x = 0.0
        message.angular.y = 0.0
        message.angular.z = -1.0
        #rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()

    else :
        message = Empty()
        message = ''
        #rospy.loginfo(message)
        pub_land.publish(message)
        rate.sleep()
    
    


def callback(position):
    global z
    
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', position)
    z = position.altitude
    



if __name__ == '__main__':
    try:
        talker_ardrone()
    except rospy.ROSInterruptException:
        pass
