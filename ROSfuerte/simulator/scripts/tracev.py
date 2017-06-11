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

global vitesse
vitesse = Twist()

global simnav
simnav = Navdata()

def tracev():

    global vitesse
    global simnav

    rospy.init_node('tracev', anonymous=True)
    
    rate = rospy.Rate(1)

    rospy.Subscriber('/cmd_vel', Twist, callback)
    rospy.Subscriber('/ardrone/navdata', Navdata, callback_navdata)

    mon_fichier_vx = open("tracevx.txt", "w")
    mon_fichier_vy = open("tracevy.txt", "w")
    mon_fichier_vz = open("tracevz.txt", "w")
    mon_fichier_simvx = open("trace_simvx.txt", "w")
    mon_fichier_simvy = open("trace_simvy.txt", "w")
    mon_fichier_simvz = open("trace_simvz.txt", "w")

    while not rospy.is_shutdown():
 
	val_vx = str(vitesse.linear.x)
	val_vy = str(vitesse.linear.y)
	val_vz = str(vitesse.linear.z)

	sim_val_vx = str(simnav.vx)
	sim_val_vy = str(simnav.vy)
	sim_val_vz = str(simnav.vz)

        mon_fichier_vx.write(val_vx + '\n')
        mon_fichier_vy.write(val_vy + '\n')
        mon_fichier_vz.write(val_vz + '\n')

        mon_fichier_simvx.write(sim_val_vx + '\n')
        mon_fichier_simvy.write(sim_val_vy + '\n')
        mon_fichier_simvz.write(sim_val_vz + '\n')

        rate.sleep()

    mon_fichier_vx.close()
    mon_fichier_vy.close()
    mon_fichier_vz.close()

    mon_fichier_simvx.close()
    mon_fichier_simvy.close()
    mon_fichier_simvz.close()


def callback(ardrone_twist):
     
    global vitesse
    vitesse = ardrone_twist

def callback_navdata(navdata):
     
    global simnav
    simnav = navdata

if __name__ == '__main__':
    try:
        tracev()
    except rospy.ROSInterruptException:
        pass
