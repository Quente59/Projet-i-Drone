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
model = ModelStates()

#ModelStates() correspond a 3 listes : name[], pose[], twist[]
#ModelState() contient name, pose, twist etc. pour un element

def talker_position():

    global model


    rospy.init_node('talker_position', anonymous=True)
    pub = rospy.Publisher('/ardrone/position', ModelStates)
    
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('/gazebo/model_states', ModelStates , callback)


    while not rospy.is_shutdown():

        pub.publish(model)
        rate.sleep()


def callback(navdata):

    global model
    model = model_states
    rospy.loginfo('MODEL STATES %s', model_states)



if __name__ == '__main__':
    try:
        talker_position()
    except rospy.ROSInterruptException:
        pass
