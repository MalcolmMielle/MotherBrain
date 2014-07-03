#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

from std_msgs.msg import *
from geometry_msgs.msg import *


from States.searchingState import *
from States.movingState import *
from States.lift import *
from States.getPose import *
from States.util import *


"""def monitor_cb(ud, msg):
	print('get in monitor')
	print "this is the message. Position : "+str(msg.position.x)+", "+str(msg.position.y)+", "+str(msg.position.z)+" Orientation : "+str(msg.orientation.x)+", "+str(msg.orientation.y)+", "+str(msg.orientation.z)+", "+str(msg.orientation.w)

	#We want a plane and orientation only around the z axis.
	 
	Quaternion : 
	q[0]=cos(r/2)
	q[1]=cos(r/2)*x
	q[2]=cos(r/2)*y
	q[3]=cos(r/2)*z

	So we 0 out the y and x

	

	if msg.position.z != 0.0 or msg.orientation.y != 0 or msg.orientation.z != 0:
		print("It's not on the ground plane, the robot can't go there. Sorry")
		return 'invalid'
	else:
		print("Good")
		return 'valid'"""
			


def main():
	rospy.init_node('MotherBrain')
	
	pose = Pose()

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	sm.userdata.sm_pose = pose #Don't know how to declare a message...
	sm.userdata.sm_object_flag=False

	print(str(sm.userdata.sm_pose.position.x))
	# Open the container
	with sm:
		# Add states to the container
		
		#smach.StateMachine.add('MoveUser', MonitorState2("/user_pose", Pose, getPositionUser) , transitions={'invalid':'MoveUser', 'valid':'End', 'preempted':'MoveUser'}, remapping={'pose_user':'sm_pose'})
		
		smach.StateMachine.add('MoveUser2', WaitForMsgState("/user_pose", Pose, getPositionUser_V2, ['pose_user'], ['pose_user']), 
		transitions={'preempted' : 'MoveUser2', 'aborted' : 'MoveUser2', 'succeeded' : 'MoveUser2'},
		remapping={'pose_user':'sm_pose'})
		# msg_cb=None, output_keys=None, latch=False, timeout=None)
		                       

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
