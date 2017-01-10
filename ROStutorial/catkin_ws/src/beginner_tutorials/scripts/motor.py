#!/usr/bin/env python


import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    
    while not rospy.is_shutdown():

	if data.data < 10:

            message = '[2.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]'

	else:
            
	    message = '[0.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]'

	rospy.loginfo(rospy.get_caller_id() + 'I said %s', message)
        pub.publish(message)
        rate.sleep()


def motor():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
   
    rospy.init_node('motor', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('pose/x', String, callback)
    pub = rospy.Publisher('cmd_vel', String, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    motor()
