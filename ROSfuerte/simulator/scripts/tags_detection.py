#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy'); roslib.load_manifest('ar_track_alvar')
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata
from ar_track_alvar.msg import AlvarMarkers

global marker_id

global compteur_marker
compteur_marker = 0

global compteur_no_marker
compteur_no_marker = 0




def tags_detection():

    global marker_id
    global compteur_marker
    global compteur_no_marker

    
    takeoff = False
    compteur_takeoff = 0
    marker_detected = False
    
    rospy.init_node('tags_detection', anonymous=True)

    
        
    pub = rospy.Publisher('/cmd_vel', Twist)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
    pub_land = rospy.Publisher('/ardrone/land', Empty)

    
    
    rate = rospy.Rate(10) # 10hz

    #rospy.Subscriber('/ardrone/navdata', Navdata, callback)
    
    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, callback)
    
   
    
    while not rospy.is_shutdown():

    	
        if not takeoff :
	
            message = Empty()
            #rospy.loginfo(message)
            pub_takeoff.publish(message)
            compteur_takeoff += 1
            rate.sleep()
    	    
            if (compteur_takeoff > 30) :
        	takeoff = True
	    	rospy.loginfo('takeoff : %s', takeoff)
            
	else:
	    #rospy.loginfo('%s',marker_detected)
	    if ((not marker_detected) and (compteur_marker > 20)):
		
		marker_detected = True
		
		rospy.loginfo('marker_detected : %s', marker_detected)
		rospy.loginfo('marker_id : %s', marker_id)

            if ((marker_detected) and (compteur_no_marker > 20)):
		
		marker_detected = False
		rospy.loginfo('marker_detected : %s', marker_detected)
		
	    if marker_detected:
		
		if (marker_id == 0):
		    twistPlusX(pub, rate)


		if (marker_id == 10):
		    twistMinusX(pub, rate)
		

def callback(data):
    global marker_id
    global compteur_marker
    global compteur_no_marker

    
    
    if (len(data.markers) == 1):
	
	marker_id = data.markers[0].id


	compteur_no_marker = 0
	compteur_marker += 1

    else :

	compteur_marker = 0
	compteur_no_marker += 1
    

def twistPlusX(pub, rate):
    message = Twist()
    message.linear.x = 0.5
    message.linear.y = 0.0
    message.linear.z = 0.0
    message.angular.x = 0.0
    message.angular.y = 0.0
    message.angular.z = 0.0
    #rospy.loginfo(message)
    pub.publish(message)
    rate.sleep()

def twistMinusX(pub, rate):
    message = Twist()
    message.linear.x = -0.5
    message.linear.y = 0.0
    message.linear.z = 0.0
    message.angular.x = 0.0
    message.angular.y = 0.0
    message.angular.z = 0.0
    #rospy.loginfo(message)
    pub.publish(message)
    rate.sleep()
        



if __name__ == '__main__':
    try:
        tags_detection()
    except rospy.ROSInterruptException:
        pass
