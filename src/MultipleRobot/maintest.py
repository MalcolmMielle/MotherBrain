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
from States.util import *
from States.getPose import *




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
	
	rospy.loginfo("Going in ;)")
	mover=GoalMaker(False,2, 60) #set at true for testing !
	rospy.loginfo("Done")
	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	sm.userdata.sm_pose_goal = list()
	sm.userdata.sm_pose_goal.append(pose) #Don't know how to declare a message...
	sm.userdata.sm_pose_goal.append(pose2) #Don't know how to declare a message...
	
	sm.userdata.sm_pose_test = list(sm.userdata.sm_pose_goal) #copy

	sm.userdata.sm_object_flag = list()
	sm.userdata.sm_object_flag.append(False)
	sm.userdata.sm_object_flag.append(False)
	
	sm.userdata.sm_pose_base=list()
	sm.userdata.sm_pose_base.append(pose_base)
	sm.userdata.sm_pose_base.append(pose_base2)
	
	sm.userdata.sm_object_flag=False
	sm.userdata.sm_iteration_get_pose=0
	sm.userdata.nb_robot=2
	
	# Open the container
	with sm: 
		# Add states to the container
		
		
		smach.StateMachine.add('Init',Move(mover), 
		transitions={'invalid':'End', 'valid':'Move', 'preempted':'End', 'invalid' : 'End', 'valid_no_object' : 'CreateGoal'}, 
		remapping={'move_pose_list':'sm_pose_base' , 'move_object_flag':'sm_object_flag'})
		
		                  
		smach.StateMachine.add('Move',Move(mover), 
		transitions={'invalid':'End', 'valid':'Lift', 'preempted':'End', 'invalid' : 'End', 'valid_no_object' : 'Lift'}, 
		remapping={'move_pose_list':'sm_pose_goal' , 'move_object_flag':'sm_object_flag'})
		
#		smach.StateMachine.add('Moveb',Move(mover), 
#		transitions={'invalid':'End', 'valid':'Move', 'preempted':'Move', 'invalid' : 'Move', 'valid_no_object' : 'Move'}, 
#		remapping={'move_pose_list':'sm_pose_base' , 'move_object_flag':'sm_object_flag'})

		smach.StateMachine.add('Lift', Lift(), 
		                      transitions={'invalid':'Lift', 'valid':'getPose', 'preempted':'Lift', 'valid_unlift' : 'Back2Base'},
		                      remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                      
		smach.StateMachine.add('getPose', WaitForMsgState("/user_pose", Pose, getPositionUser_V2, ['pose_user', 'pose_iteration', 'nb_robot'], ['pose_user', 'pose_iteration']), 
		transitions={'preempted' : 'getPose', 'aborted' : 'End', 'succeeded' : 'Move'},
		remapping={'pose_user':'sm_pose_goal' , 'pose_iteration' : 'sm_iteration_get_pose', 'nb_robot' : 'nb_robot'})
		
		#Init should be suppress in some way so we only use Move...(or not?) Using init for testing purpose
		smach.StateMachine.add('Back2Base', Back2Base(), 
		transitions={'invalid':'Back2Base', 'valid':'Init', 'preempted':'Back2Base'}, 
		remapping={'pose':'sm_pose_goal' , 'pose_base' : 'sm_pose_base'})

		smach.StateMachine.add('CreateGoal', Back2Base(), 
		transitions={'invalid':'Back2Base', 'valid':'Move', 'preempted':'Back2Base'}, 
		remapping={'pose':'sm_pose_goal' , 'pose_base' : 'sm_pose_test'})                     
		                  

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
