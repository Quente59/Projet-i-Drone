#!/usr/bin/env python
# license removed for brevity
import numpy as np
import matplotlib.pyplot as plt

import rospy
import roslib; roslib.load_manifest('ardrone_autonomy'); roslib.load_manifest('gazebo')
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import *
from ardrone_autonomy.msg import Navdata

from gazebo.srv import *
from gazebo.msg import *
from gazebo_msgs.msg import *

global pos
pos = Pose()

def tracexy():

    global position

    mon_fichier_x = open("tracex.txt", "r")
    mon_fichier_y = open("tracey.txt", "r")

    mon_fichier_x.close()
    mon_fichier_y.close()

    rospy.init_node('tracexy', anonymous=True)
    
    rate = rospy.Rate(2)

    rospy.Subscriber('/ardrone/position', Pose , callback)

    mon_fichier_x = open("tracex.txt", "w")
    mon_fichier_y = open("tracey.txt", "w")

    while not rospy.is_shutdown():
	
	val_x = str(pos.position.x)
	val_y = str(pos.position.y)

        mon_fichier_x.write(val_x + '\n')
        mon_fichier_y.write(val_y + '\n')

        rate.sleep()

    mon_fichier_x.close()
    mon_fichier_y.close()

def callback(position):

        pos.position.x = position.position.x
	pos.position.y = position.position.y


if __name__ == '__main__':
    try:
        tracexy()
    except rospy.ROSInterruptException:
        pass