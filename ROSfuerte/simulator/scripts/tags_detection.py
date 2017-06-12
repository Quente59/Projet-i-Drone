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
    altitude = 1500.0
    changeAltd = True

    offset_ori_z = 0.0

    task_0_done = False
    task_13_done = False
    task_7_done = False
    task_4_done = False
    task_14_done = False
    task_9_done = False

    pos_tag_0 = [[0.0,0.0],[2.0,-6.0],[4.0,-8.0]]
    compteur_tag_0 = 0
    pos_tag_10 = [[4.0,0.0],[0.0,-6.0],[-6.0,-6.0],[-6.0,0.0]]
    compteur_tag_10 = 0
    pos_tag_7 = [[6.0,-4.0]]
    compteur_tag_7 = 0
    pos_tag_13 = [[4.0,-4.0],[4.0,-4.0]]
    compteur_tag_13 = 0
    pos_tag_4 = [[4.0,-6.0],[4.0,-10.0]]
    compteur_tag_4 = 0
    pos_tag_14 = [[2.0,-8.0]]
    compteur_tag_14 = 0
    pos_tag_9 = [[0.0,-10.0]]
    compteur_tag_9 = 0
    pos_tag_3 = [[-2.0,-6.0]]
    compteur_tag_3 = 0
    pos_tag_6 = [[-4.0,-6.0]]
    compteur_tag_6 = 0
    

    inRotation = False
    task_10_done = False
    coef_rotation = 1.0
    position_corrected = False
    orientation_corrected = False

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
		task_4_done = False
		task_14_done = False
		task_9_done = False
		task_3_done = False
		task_6_done = False
		
	    if marker_detected:

		compteur_timer = 0.0
		
		if (marker_id == 0):
		    
		    if not task_0_done:
		        while not (position_corrected and orientation_corrected):
			    #rospy.loginfo("adjusting position and orientation")
			    position_corrected = ajustement_position(pos_tag_0[compteur_tag_0][0], pos_tag_0[compteur_tag_0][1])
			    orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()
			
			task_0_done = True
			compteur_tag_0 +=1
			position_corrected = False
			orientation_corrected = False

		    twistPlusX()

		if (marker_id == 4):
		    
		    if not task_4_done:
		        while not (position_corrected and orientation_corrected):
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_4[compteur_tag_4][0], pos_tag_4[compteur_tag_4][1])
			    orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()
			
			task_4_done = True
			compteur_tag_4 +=1
			position_corrected = False
			orientation_corrected = False

		    twistMinusY()

		if (marker_id == 9):
		    
		    if not task_9_done:
		        while not (position_corrected and orientation_corrected):
			    #rospy.loginfo("adjusting position and orientation")
			    position_corrected = ajustement_position(pos_tag_9[compteur_tag_9][0], pos_tag_9[compteur_tag_9][1])
			    orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()
			
			task_9_done = True
			compteur_tag_9 +=1
			position_corrected = False
			orientation_corrected = False

		    twistMinusX()

		if (marker_id == 14):
		    
		    if not task_14_done:
		        while not (position_corrected and orientation_corrected):
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_14[compteur_tag_14][0], pos_tag_14[compteur_tag_14][1])
			    orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()
			
			task_14_done = True
			compteur_tag_14 +=1
			position_corrected = False
			orientation_corrected = False

		    twistPlusY()

		if (marker_id == 7):

		    if not task_7_done:    #-180degres
			
			
			while not position_corrected:
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_7[compteur_tag_7][0], pos_tag_7[compteur_tag_7][1])
			    
			    correction_altd(correction_altd_ON, altitude)
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
				compteur_tag_7 +=1
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
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_13[compteur_tag_13][0], pos_tag_13[compteur_tag_13][1])
			    
			    correction_altd(correction_altd_ON, altitude)
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
				compteur_tag_13 +=1
			        position_corrected = False
				orientation += 90.0
				inRotation = False
				offset_ori_z = 1.0
			        enable_ori_z = True
				#coef_rotation -= coef_rotation
			        message_twist.angular.z = 0.0
                    
		    else:
			twistPlusX()
		if (marker_id == 12):

		    rospy.loginfo("on the way")

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
			
			if abs(orientation) == 0.0:
			    test1 = 0.25
			    test2 = 0.68
			    coef = 1.0

			elif abs(orientation) == 90.0:
			    test1 = 0.80
			    test2 = 0.999
			    coef = 1.0

			elif abs(orientation) == 180.0:
			    test1 = -0.80
			    test2 = -0.70
			    coef = -1.0

			elif abs(orientation) == 270.0:
			    test1 = -0.68
			    test2 = -0.25
			    coef = -1.0
			
			while not position_corrected:
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_10[compteur_tag_10][0], pos_tag_10[compteur_tag_10][1])
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()

         		if not inRotation:
			
			    enable_ori_z = False
		            twistAngularZ()
			    message_twist.linear.x = 0.0
    			    message_twist.linear.y = 0.0

			    if coef*abs(message_position.orientation.z) > test1:
			        inRotation = True

		        else:
			    twistAngularZ()
			    message_twist.linear.x = 0.0
   			    message_twist.linear.y = 0.0
			    if coef*abs(message_position.orientation.z) > test2:
			        task_10_done = True
				compteur_tag_10 +=1
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

		if (marker_id == 3): #down

		    if not task_3_done:
		        while not (position_corrected):# and orientation_corrected):
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_3[compteur_tag_3][0], pos_tag_3[compteur_tag_3][1])
			    #orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()

			correction_altd_ON = False
			
			if changeAltd :
			
			    halfAltd = 1000.0
			    changeAltd = False

			if (message_altd > halfAltd):
			    rospy.loginfo("je descends")
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
			    message_twist.angular.z = 0.0
			    twistMinusZ()

			else :
			    altitude = halfAltd
			    correction_altd_ON = True
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
			    message_twist.angular.z = 0.0
			    twistPlusX()

			    task_3_done = True
		    	    compteur_tag_3 +=1
			    position_corrected = False
			    orientation_corrected = False
			    changeAltd = True
			

		if (marker_id == 6): #up

		    if not task_6_done:
		        while not (position_corrected): #and orientation_corrected):
			    #rospy.loginfo("adjusting position")
			    position_corrected = ajustement_position(pos_tag_6[compteur_tag_6][0], pos_tag_6[compteur_tag_6][1])
			    #orientation_corrected = ajustement_orientation()
			    correction_altd(correction_altd_ON, altitude)
			    pub.publish(message_twist)
			    rate.sleep()
			
			correction_altd_ON = False
			
			if changeAltd :

			    doubleAltd = 1500.0
			    changeAltd = False

			if (message_altd < doubleAltd):
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
			    message_twist.angular.z = 0.0
			    twistPlusZ()
			    

			else :
			    altitude = doubleAltd
			    correction_altd_ON = True
			    message_twist.linear.x = 0.0
			    message_twist.linear.y = 0.0
			    message_twist.angular.z = 0.0
			    twistPlusX()

			    task_6_done = True
		    	    compteur_tag_6 +=1
			    position_corrected = False
			    orientation_corrected = False
			    changeAltd = True


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
		

	    correction_altd(correction_altd_ON, altitude)           
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
    message_twist.linear.x = 0.6
    
def twistMinusX():

    global message_twist
    message_twist.linear.x = -0.6

def twistPlusY():

    global message_twist
    message_twist.linear.y = 0.6
    
def twistMinusY():

    global message_twist
    message_twist.linear.y = -0.6

def twistMinusZ():

    global message_twist
    message_twist.linear.z = -0.6

def twistPlusZ():

    global message_twist
    message_twist.linear.z = 0.4

def twistAngularZ():

    global message_twist
    message_twist.angular.z = -0.4

def twistPlusAngularZ():

    global message_twist
    message_twist.angular.z = 0.6

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

    speed_ajustement = 0.07
    delta_ajustement = 0.02
      
    if orientation == 0.0:
	if message_position.position.x > pos_tag_x + delta_ajustement:
	    message_twist.linear.x = -speed_ajustement
            position_x_okay = False

        if message_position.position.x < pos_tag_x - delta_ajustement:
       	    message_twist.linear.x = speed_ajustement
	    position_x_okay = False

        if (message_position.position.x > pos_tag_x - delta_ajustement) and (message_position.position.x < pos_tag_x + delta_ajustement):
	    message_twist.linear.x = 0.0
	    position_x_okay = True
 
   
        if message_position.position.y > pos_tag_y + delta_ajustement:
	    message_twist.linear.y = -speed_ajustement
	    position_y_okay = False

        if message_position.position.y < pos_tag_y - delta_ajustement:
	    message_twist.linear.y = speed_ajustement
	    position_y_okay = False

        if (message_position.position.y > pos_tag_y - delta_ajustement) and (message_position.position.y < pos_tag_y + delta_ajustement):
            message_twist.linear.y = 0.0
	    position_y_okay = True

        if position_x_okay and position_y_okay:
	    rospy.loginfo("position adjusted")
	    return True
        else:
	    return False
	
    elif orientation == -90.0:
	if message_position.position.x > pos_tag_x + delta_ajustement:
	    message_twist.linear.y = -speed_ajustement
            position_x_okay = False

        if message_position.position.x < pos_tag_x - delta_ajustement:
	    message_twist.linear.y = speed_ajustement
	    position_x_okay = False

        if (message_position.position.x > pos_tag_x - delta_ajustement) and (message_position.position.x < pos_tag_x + delta_ajustement):
	    message_twist.linear.y = 0.0
	    position_x_okay = True
 
   
        if message_position.position.y > pos_tag_y + delta_ajustement:
	    message_twist.linear.x = speed_ajustement
	    position_y_okay = False

        if message_position.position.y < pos_tag_y - delta_ajustement:
	    message_twist.linear.x = -speed_ajustement
	    position_y_okay = False

        if (message_position.position.y > pos_tag_y - delta_ajustement) and (message_position.position.y < pos_tag_y + delta_ajustement):
            message_twist.linear.x = 0.0
	    position_y_okay = True

        if position_x_okay and position_y_okay:
	    rospy.loginfo("position adjusted")
	    return True
        else:
	    return False

    if (orientation == -180.0) or (orientation == 180.0):
	if message_position.position.x > pos_tag_x + delta_ajustement:
	    message_twist.linear.x = speed_ajustement
            position_x_okay = False

        if message_position.position.x < pos_tag_x - delta_ajustement:
       	    message_twist.linear.x = -speed_ajustement
	    position_x_okay = False

        if (message_position.position.x > pos_tag_x - delta_ajustement) and (message_position.position.x < pos_tag_x + delta_ajustement):
	    message_twist.linear.x = 0.0
	    position_x_okay = True
 
   
        if message_position.position.y > pos_tag_y + delta_ajustement:
	    message_twist.linear.y = speed_ajustement
	    position_y_okay = False

        if message_position.position.y < pos_tag_y - delta_ajustement:
	    message_twist.linear.y = -speed_ajustement
	    position_y_okay = False

        if (message_position.position.y > pos_tag_y - delta_ajustement) and (message_position.position.y < pos_tag_y + delta_ajustement):
            message_twist.linear.y = 0.0
	    position_y_okay = True

        if position_x_okay and position_y_okay:
	    rospy.loginfo("position adjusted")
	    return True
        else:
	    return False
	

def ajustement_orientation():

    global message_position
    global message_twist

    orientation_okay = False
    
      
    if orientation == 0.0:
	if message_position.orientation.z > 0.01:
	    message_twist.angular.z = -0.05
            orientation_okay = False

        if message_position.orientation.z < -0.01:
       	    message_twist.angular.z = 0.05
	    orientation_okay = False

        if (message_position.orientation.z > -0.01) and (message_position.orientation.z < 0.01):
	    message_twist.angular.z = 0.0
	    orientation_okay = True

        if orientation_okay:
	    rospy.loginfo("orientation adjusted")
	    return True
        else:
	    return False
	
    if orientation == -90.0:
	if abs(message_position.orientation.z) > 0.73:
	    message_twist.angular.z = 0.05
            orientation_okay = False

        if abs(message_position.orientation.z) < 0.71:
       	    message_twist.angular.z = -0.05
	    orientation_okay = False

        if (abs(message_position.orientation.z) > 0.71) and (abs(message_position.orientation.z) < 0.73):
	    message_twist.angular.z = 0.0
	    orientation_okay = True

        if orientation_okay:
	    rospy.loginfo("orientation adjusted")
	    return True
        else:
	    return False

   

def correction_altd(correction_altd_ON, altitude):

    global message_altd
    global message_twist 

    if correction_altd_ON:
        if message_altd > (altitude + 50.0):
	    message_twist.linear.z = -0.05

	if message_altd < (altitude - 50.0):
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
