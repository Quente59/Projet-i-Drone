#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy'); roslib.load_manifest('ar_track_alvar')
from geometry_msgs.msg import Twist, Pose
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata
from ar_track_alvar.msg import AlvarMarkers

global marker_id

global compteur_marker
compteur_marker = 0

global compteur_no_marker
compteur_no_marker = 0

global message_twist
message_twist = Twist()

global message_position
message_position = Pose()

global message_altd
message_altd = 0.0




def tags_detection():

    global marker_id
    global compteur_marker
    global compteur_no_marker

    global message_twist
    global message_position
    global message_altd

    mem_altd = 0.0
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

    rospy.Subscriber('/cmd_vel', Twist, callback_twist)

    rospy.Subscriber('/ardrone/position', Pose, callback_position)

    rospy.Subscriber('/ardrone/navdata', Navdata, callback_altd)
    
   
    
    while not rospy.is_shutdown():

    	
        if not takeoff :
	
            if (compteur_takeoff < 40):

	        message_takeoff = Empty()
		#rospy.loginfo(message)
		pub_takeoff.publish(message_takeoff)
		compteur_takeoff += 1
                mem_altd = message_twist.linear.z
		rate.sleep()
		
    	    
            else: 
		
		if (message_altd < 1500):
		    message_twist.linear.z = 0.5
		    pub.publish(message_twist)
	            rate.sleep()

		else :
		    message_twist.linear.z = mem_altd
		    pub.publish(message_twist)
        	    takeoff = True
	    	    rospy.loginfo('takeoff : %s', takeoff)
		    rospy.Rate(1).sleep()
		    
            
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
		    twistPlusX()


		if (marker_id == 10):
		    twistMinusX()

            correction_trajectoire()

	    pub.publish(message_twist)
            rate.sleep()
		

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

def callback_twist(ardrone_twist):
    global message_twist


    message_twist = ardrone_twist

def callback_position(ardrone_position):

    global message_position
    
    message_position = ardrone_position

def callback_altd(ardrone_altd):

    global message_altd

    message_altd = ardrone_altd.altd    

def twistPlusX():

    global message_twist
    message_twist.linear.x = 0.5
    

def twistMinusX():

    global message_twist
    message_twist.linear.x = -0.5
    

def correction_trajectoire():

    global message_position
    global message_twist

    if message_position.orientation.z > 0.01:
        message_twist.angular.z = -0.05

    if message_position.orientation.z < -0.01:
        message_twist.angular.z = 0.05

    if message_position.position.y > 0.01:
        message_twist.linear.y = -0.05

    if message_position.position.y < -0.01:
        message_twist.linear.y = 0.05

    
        



if __name__ == '__main__':
    try:
        tags_detection()
    except rospy.ROSInterruptException:
        pass
