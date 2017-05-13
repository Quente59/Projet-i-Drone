#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy'); roslib.load_manifest('ar_track_alvar')
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata
from ar_track_alvar.msg import AlvarMarkers

global markers

global compteur_markers
compteur_markers = 0




def talker_ardrone():

    global markers
    takeoff = False
    compteur = 0
    marker_detected = False
    
    rospy.init_node('tags_detection', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
    pub_land = rospy.Publisher('/ardrone/land', Empty)

    
    
    rate = rospy.Rate(10) # 10hz

    #rospy.Subscriber('/ardrone/navdata', Navdata, callback)
    
    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, callback)
    
   
    
    while not rospy.is_shutdown():

    	rospy.loginfo('%s',marker_detected)
        if not takeoff :

            message = Empty()
            #rospy.loginfo(message)
            pub_takeoff.publish(message)
	    compteur += 1
	    rate.sleep()
	    #rospy.loginfo('%s',compteur)
	    
            if (compteur > 30) :
 	    	takeoff = True
        
	    	

	else:
	    
	    if (compteur_markers > 10):
		marker_detected = True
		
	    if marker_detected:
		message = Twist()
	        message.linear.x = 0.0
	        message.linear.y = 0.0
	        message.linear.z = 0.0
	        message.angular.x = 0.0
	        message.angular.y = 0.0
	        message.angular.z = -0.5
	        #rospy.loginfo(message)
	        pub.publish(message)
	        rate.sleep()

		
		

	

	    
    


def callback(data):
    global markers
    global compteur_markers
    
    if (len(data.markers) == 1):

        #rospy.loginfo('%s', data.markers[0].id)
	compteur_markers += 1

    else:
	compteur_markers = 0
    
	
    
    



if __name__ == '__main__':
    try:
        talker_ardrone()
    except rospy.ROSInterruptException:
        pass
