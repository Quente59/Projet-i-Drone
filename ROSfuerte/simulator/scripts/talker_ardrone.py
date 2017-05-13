#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy')
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata

global z
z = 0





def talker_ardrone():

    global z
    takeoff = False
    compteur = 0
    
    rospy.init_node('talker_ardrone', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
    pub_land = rospy.Publisher('/ardrone/land', Empty)
    
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/ardrone/navdata', Navdata, callback)
    
   
    
    while not rospy.is_shutdown():

    	
        if z < 2000 :

	    message = Twist()
	    message.linear.x = 0.0
	    message.linear.y = 0.0
	    message.linear.z = 1.0
	    message.angular.x = 0.0
            message.angular.y = 0.0
            message.angular.z = 0.0
	    #rospy.loginfo(message)
	    pub.publish(message)
	    rate.sleep()


	else :

       	    message = Twist()
	    message.linear.x = 0.0
	    message.linear.y = 0.0
	    message.linear.z = 0.0
	    message.angular.x = 0.0
	    message.angular.y = 0.0
	    message.angular.z = 0.0
	    #rospy.loginfo(message)
	    pub.publish(message)
	    rate.sleep()

	    
    


def callback(navdata):
    global z
    
    #rospy.loginfo('Altitude %s', navdata.altd)
	
    z = navdata.altd
    



if __name__ == '__main__':
    try:
        talker_ardrone()
    except rospy.ROSInterruptException:
        pass
