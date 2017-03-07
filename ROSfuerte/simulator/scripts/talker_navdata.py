#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib; roslib.load_manifest('ardrone_autonomy')
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata

global message
message = Navdata()

def talker_navdata():

    global message

    rospy.init_node('talker_navdata', anonymous=True)
    pub = rospy.Publisher('/ardrone/navdata_modified', Navdata)
    
    rate = rospy.Rate(100) # 100hz

    rospy.Subscriber('/ardrone/navdata', Navdata, callback)


    while not rospy.is_shutdown():

        pub.publish(message)
        rate.sleep()


def callback(navdata):

    global message
    
    navdata.tags_count = 1
    #navdata.tags_type[0] = 0
    navdata.tags_xc = (0,0)
    navdata.tags_yc = (0,0)
    navdata.tags_width = (0,0)
    navdata.tags_height = (0,0)
    navdata.tags_orientation = (0.0, 0.0)
    navdata.tags_distance = (0.0, 0.0)

    message = navdata
    



if __name__ == '__main__':
    try:
        talker_navdata()
    except rospy.ROSInterruptException:
        pass
