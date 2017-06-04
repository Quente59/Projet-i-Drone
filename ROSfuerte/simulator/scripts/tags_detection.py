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

global compteur_timer
compteur_timer = 0.0

global time_ref
time_ref = 0.0


def tags_detection():

    global marker_id
    global compteur_marker
    global compteur_no_marker

    global message_twist
    global message_position
    global message_altd

    
    global orientation
    orientation = 0.0

    global compteur_timer
    global time_ref

    mem_altd = 0.0
    takeoff = False
    compteur_takeoff = 0
    marker_detected = False
    
    rospy.init_node('tags_detection', anonymous=True)

    
        
    pub = rospy.Publisher('/cmd_vel', Twist)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
    pub_land = rospy.Publisher('/ardrone/land', Empty)

    enable_ori_z = True
    enable_pos_y = True
    correction_altd_ON = True

    offset_ori_z = 0.0

    task_0_done = False
    task_13_done = False
    task_7_done = False

    inRotation = False
    task_10_done = False
    coef_rotation = 1.0
    position_corrected = False

    rate = rospy.Rate(10) # 10hz

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

		task_10_done = False
		task_0_done = False
    		task_13_done = False
    		task_7_done = False
		
	    if marker_detected:

		compteur_timer = 0.0
		
		if (marker_id == 0):
		    
		    if not task_0_done:
		        while not position_corrected:
			    rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(0.0, 0.0)
			    correction_altd(correction_altd_ON)
			    pub.publish(message_twist)
			    rate.sleep()
			
			task_0_done = True
			position_corrected = False

		    twistPlusX()



		if (marker_id == 7):

		    if not task_7_done:    #-180degres
			
			
			while not position_corrected:
			    rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(6.0, -4.0)
			    
			    correction_altd(correction_altd_ON)
			    pub.publish(message_twist)
			    rate.sleep()

         		if not inRotation:
			
			    enable_ori_z = False
		            twistAngularZ()
			    message_twist.linear.x = 0.0
    			    message_twist.linear.y = 0.0

			    if abs(message_position.orientation.z) > 0.5:
			        inRotation = True

		        else:
			    twistAngularZ()
			    message_twist.linear.x = 0.0
   			    message_twist.linear.y = 0.0
			    if abs(message_position.orientation.z) > 0.999:
			        task_7_done = True
				
			        position_corrected = False
				orientation -= 180.0
				inRotation = False
				offset_ori_z = 1.0
			        enable_ori_z = True
				#coef_rotation -= coef_rotation
			        message_twist.angular.z = 0.0
                    
		    else:
			twistPlusX()

		if (marker_id == 13):

		    if not task_13_done:    #+90degres
			
			if abs(orientation) == 90.0:
			    test1 = 0.25
			    test2 = 0.1

			elif abs(orientation) == 180.0:
			    test1 = 0.80
			    test2 = 0.70


			while not position_corrected:
			    rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(4.0, -4.0)
			    
			    correction_altd(correction_altd_ON)
			    pub.publish(message_twist)
			    rate.sleep()

         		if not inRotation:
			
			    enable_ori_z = False
		            twistPlusAngularZ()
			    message_twist.linear.x = 0.0
    			    message_twist.linear.y = 0.0

			    if abs(message_position.orientation.z) < test1:
			        inRotation = True

		        else:
			    twistPlusAngularZ()
			    message_twist.linear.x = 0.0
   			    message_twist.linear.y = 0.0
			    if abs(message_position.orientation.z) < test2:
			        task_13_done = True
			        position_corrected = False
				orientation += 90.0
				inRotation = False
				offset_ori_z = 1.0
			        enable_ori_z = True
				#coef_rotation -= coef_rotation
			        message_twist.angular.z = 0.0
                    
		    else:
			twistPlusX()

		if (marker_id == 10):

		    '''enable_pos_y = False
		    twistPlusY()'''

		    '''if not task_10_done:	#-360degres

			
         		if not inRotation:
			
			    enable_ori_z = False
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
		            twistAngularZ()

			    if abs(message_position.orientation.z) > 0.5:
			        inRotation = True

		        else:
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
			    twistAngularZ()
			    if abs(message_position.orientation.z) < 0.05:
			        task_10_done = True
				inRotation = False
			        enable_ori_z = True
				coef_rotation -= coef_rotation
			        message_twist.angular.z = 0.0
                    
		    else:
			twistMinusX()'''



		    if not task_10_done:    #-90degres
			
			
			while not position_corrected:
			    rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(4.0, 0.0)
			    correction_altd(correction_altd_ON)
			    pub.publish(message_twist)
			    rate.sleep()

         		if not inRotation:
			
			    enable_ori_z = False
		            twistAngularZ()
			    message_twist.linear.x = 0.0
    			    message_twist.linear.y = 0.0

			    if abs(message_position.orientation.z) > 0.25:
			        inRotation = True

		        else:
			    twistAngularZ()
			    message_twist.linear.x = 0.0
   			    message_twist.linear.y = 0.0
			    if abs(message_position.orientation.z) > 0.65:
			        task_10_done = True
			        position_corrected = False
				orientation -= 90.0
				inRotation = False
				offset_ori_z = 1.0
			        enable_ori_z = True
				#coef_rotation -= coef_rotation
			        message_twist.angular.z = 0.0
                    
		    

		    else:
			twistPlusX()
			
			#orientation_z_mem = message_position.orientation.z


	    compteur_timer += 1
	    #rospy.loginfo('time : %s', compteur_timer)
	        
	    if (compteur_timer >= 50):
		
		#stop(pub, rate)
		landing(pub_land, rate)

		while (message_altd > 100):
		
		    rospy.loginfo('landing')
		    rate.sleep()
		
		rospy.loginfo('landed')
		rospy.signal_shutdown('no more tag')
		

	    correction_altd(correction_altd_ON)           
            #correction_trajectoire(enable_pos_y)
	    #correction_orientation(coef_rotation, offset_ori_z, enable_ori_z)

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

def twistPlusY():

    global message_twist
    message_twist.linear.y = 0.5
    
def twistMinusY():

    global message_twist
    message_twist.linear.y = -0.5

def twistAngularZ():

    global message_twist
    message_twist.angular.z = -1.0

def twistPlusAngularZ():

    global message_twist
    message_twist.angular.z = 1.0

'''def goDownZ():
    global message_twist
    saveTwist = message_twist
    halfAltd = message_altd/2
    enable_pos_z = False    
    while (message_altd > halfAltd):
        message_twist.linear.x = 0.0
        message_twist.linear.y = 0.0
        message_twist.linear.z = -1.0
    
    message_twist = saveTwist
    enable_pos_z = True'''

def stop(pub, rate):

    global message_twist
    message_twist.linear.x = 0.0
    message_twist.linear.y = 0.0
    message_twist.linear.z = 0.0
    message_twist.angular.x = 0.0
    message_twist.angular.y = 0.0
    message_twist.angular.z = 0.0
    pub.publish(message_twist)
    rate.sleep()

def takingoff(pub, rate) :

    message = Empty()
    pub.publish(message)
    rate.sleep()
    
def landing(pub, rate):

    message = Empty()
    pub.publish(message)
    rate.sleep()

def ajustement_position(pos_tag_x, pos_tag_y):

    global message_position
    global message_twist

    position_x_okay = False
    position_y_okay = False
      
    if orientation == 0.0:
	if message_position.position.x > pos_tag_x + 0.01:
	    message_twist.linear.x = -0.05
            position_x_okay = False

        if message_position.position.x < pos_tag_x - 0.01:
       	    message_twist.linear.x = 0.05
	    position_x_okay = False

        if (message_position.position.x > pos_tag_x - 0.01) and (message_position.position.x < pos_tag_x + 0.01):
	    message_twist.linear.x = 0.0
	    position_x_okay = True
 
   
        if message_position.position.y > pos_tag_y + 0.01:
	    message_twist.linear.y = -0.05
	    position_y_okay = False

        if message_position.position.y < pos_tag_y - 0.01:
	    message_twist.linear.y = 0.05
	    position_y_okay = False

        if (message_position.position.y > pos_tag_y - 0.01) and (message_position.position.y < pos_tag_y + 0.01):
            message_twist.linear.y = 0.0
	    position_y_okay = True

        if position_x_okay and position_y_okay:
	    rospy.loginfo("position adjusted")
	    return True
        else:
	    return False
	
    elif orientation == -90.0:
	if message_position.position.x > pos_tag_x + 0.01:
	    message_twist.linear.y = -0.05
            position_x_okay = False

        if message_position.position.x < pos_tag_x - 0.01:
	    message_twist.linear.y = 0.05
	    position_x_okay = False

        if (message_position.position.x > pos_tag_x - 0.01) and (message_position.position.x < pos_tag_x + 0.01):
	    message_twist.linear.y = 0.0
	    position_x_okay = True
 
   
        if message_position.position.y > pos_tag_y + 0.01:
	    message_twist.linear.x = 0.05
	    position_y_okay = False

        if message_position.position.y < pos_tag_y - 0.01:
	    message_twist.linear.x = -0.05
	    position_y_okay = False

        if (message_position.position.y > pos_tag_y - 0.01) and (message_position.position.y < pos_tag_y + 0.01):
            message_twist.linear.x = 0.0
	    position_y_okay = True

        if position_x_okay and position_y_okay:
	    rospy.loginfo("position adjusted")
	    return True
        else:
	    return False
	


def correction_altd(correction_altd_ON):

    global message_altd
    global message_twist 

    if correction_altd_ON:
        if message_altd > 1550:
	    message_twist.linear.z = -0.05

	if message_altd < 1450:
	    message_twist.linear.z = 0.05 
    
def correction_trajectoire(enable_pos_y):

    global message_position
    global message_twist

    if enable_pos_y:

	if message_position.position.y > 0.01:
	    message_twist.linear.y = -0.05

	if message_position.position.y < -0.01:
	    message_twist.linear.y = 0.05


def correction_orientation(coef_rotation, offset_ori_z, enable_ori_z):

    global orientation
    global orientation_changed

    if enable_ori_z:

	
	if offset_ori_z == 1:

	    if abs(message_position.orientation.z) < offset_ori_z - 0.001:
	        message_twist.angular.z = 0.05*orientation
		orientation_changed = False

	    if not (orientation_changed) and (abs(message_position.orientation.z) > offset_ori_z - 0.001):
		orientation -= orientation
		orientation_changed = True
	else:
	    if message_position.orientation.z > 0.01:
	        message_twist.angular.z = -0.05*coef_rotation

	    if message_position.orientation.z < - 0.01:
	        message_twist.angular.z = 0.05*coef_rotation
	    
        



if __name__ == '__main__':
    try:
        tags_detection()
    except rospy.ROSInterruptException:
        pass
