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
	
	pose = PoseStamped()
	pose.pose.position.x=2
	pose.pose.orientation.w=1
	
	pose2 = PoseStamped()
	pose2.pose.position.x=2
	pose2.pose.position.y=2
	pose2.pose.orientation.w=1
	
	pose_base = PoseStamped()
	pose_base2 = PoseStamped()
	pose_base2.pose.position.y=2
	pose_base.pose.orientation.w=1
	pose_base2.pose.orientation.w=1

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	
	sm.userdata.sm_pose_goal = list()
	sm.userdata.sm_pose_goal.append(pose) #Don't know how to declare a message...
	sm.userdata.sm_pose_goal.append(pose2) #Don't know how to declare a message...
	
	sm.userdata.sm_object_flag = list()
	sm.userdata.sm_object_flag.append(False)
	sm.userdata.sm_object_flag.append(False)
	
	sm.userdata.sm_pose_base=list()
	sm.userdata.sm_pose_base.append(pose_base)
	sm.userdata.sm_pose_base.append(pose_base2)
	
	
	sm.userdata.sm_iteration_get_pose=0
	sm.userdata.nb_robot=2
	sm.userdata.stack=Stack(0.5, 0.5)

	# Open the container
	with sm:
		# Add states to the container
		
		#smach.StateMachine.add('MoveUser', MonitorState2("/user_pose", Pose, getPositionUser) , transitions={'invalid':'MoveUser', 'valid':'End', 'preempted':'MoveUser'}, remapping={'pose_user':'sm_pose'})
		
		#Preempted used has you must ask more position from user
		#Get pose from the user
		smach.StateMachine.add('getPose', WaitForMsgState("/user_pose", Pose, getPositionUser_V2, ['pose_user', 'pose_iteration', 'nb_robot', 'stack'], ['pose_user', 'pose_iteration']), 
		transitions={'preempted' : 'getPose', 'aborted' : 'getPose', 'succeeded' : 'End'},
		remapping={'pose_user':'sm_pose_goal' , 'pose_iteration' : 'sm_iteration_get_pose', 'nb_robot' : 'nb_robot', 'stack' : 'stack'})
		# msg_cb=None, output_keys=None, latch=False, timeout=None)
		                       

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
