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
from States.back2Base import *




def main():
	rospy.init_node('MotherBrain')
	
	pose = PoseStamped()
	pose.header.frame_id="/map"
	pose.pose.position.x=1
	pose.pose.orientation.w=1
	
	pose2 = PoseStamped()
	pose2.header.frame_id="/map"
	pose2.pose.position.x=1
	pose2.pose.position.y=2
	pose2.pose.orientation.w=1
	
	pose_base = PoseStamped()
	pose_base.header.frame_id="/map"
	pose_base2 = PoseStamped()
	pose_base2.header.frame_id="/map"
	pose_base.pose.position.x=-1
	pose_base2.pose.position.x=-1
	pose_base2.pose.position.y=2
	pose_base.pose.orientation.w=1
	pose_base2.pose.orientation.w=1
	
	rospy.loginfo("Going in ;)")
	mover=GoalMaker(False,2, 60) #set at true for testing !
	rospy.loginfo("Done")
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
	# Open the container
	with sm: 
		# Add states to the container
		                  
		smach.StateMachine.add('Move',Move(mover), 
		transitions={'invalid':'End', 'valid':'Moveb', 'preempted':'End', 'invalid' : 'End', 'valid_no_object' : 'End'}, 
		remapping={'move_pose_list':'sm_pose_goal' , 'move_object_flag':'sm_object_flag'})
		
		smach.StateMachine.add('Moveb',Move(mover), 
		transitions={'invalid':'End', 'valid':'Move', 'preempted':'Move', 'invalid' : 'Move', 'valid_no_object' : 'Move'}, 
		remapping={'move_pose_list':'sm_pose_base' , 'move_object_flag':'sm_object_flag'})

		                      
		                  

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
