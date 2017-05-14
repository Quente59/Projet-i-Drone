#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy'); roslib.load_manifest('gazebo')
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import *

from gazebo.srv import *
from gazebo.msg import *
from gazebo_msgs.msg import *


global model
model = ModelState()

#ModelStates() correspond a 3 listes : name[], pose[], twist[]
#ModelState() contient name, pose, twist etc. pour un element

def talker_position():

    global model


    rospy.init_node('talker_position', anonymous=True)
    pub = rospy.Publisher('/ardrone/position', ModelState)
    
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/gazebo/model_states', ModelStates , callback)


    while not rospy.is_shutdown():

        pub.publish(model)
        rate.sleep()


def callback(model_states):

    global model
    for i in range(len(model_states.name)):
	if (model_states.name[i] == 'quadrotor'):
    	    model.model_name = model_states.name[i]
	    model.pose = model_states.pose[i]
	    model.twist = model_states.twist[i]



if __name__ == '__main__':
    try:
        talker_position()
    except rospy.ROSInterruptException:
        pass
