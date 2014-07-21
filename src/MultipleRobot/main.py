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
	pose.pose.position.x=0
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
	mover=GoalMaker(False,1, 60) #set at true for testing !
	rospy.loginfo("Done")
	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	sm.userdata.sm_pose_goal = list()
	sm.userdata.sm_pose_goal.append(pose) #Don't know how to declare a message...
	#sm.userdata.sm_pose_goal.append(pose2) #Don't know how to declare a message...
	
	sm.userdata.sm_pose_test = list(sm.userdata.sm_pose_goal) #copy

	sm.userdata.sm_object_flag = list()
	sm.userdata.sm_object_flag.append(False)
	#sm.userdata.sm_object_flag.append(False)
	
	sm.userdata.sm_pose_base=list()
	sm.userdata.sm_pose_base.append(pose_base)
	#sm.userdata.sm_pose_base.append(pose_base2)
	
	sm.userdata.sm_object_flag=False
	sm.userdata.sm_iteration_get_pose=0
	sm.userdata.nb_robot=1
	
	# Open the container
	with sm: 
		# Add states to the container
		
		#Send back the object to the base before launching the search
		smach.StateMachine.add('Init',Move(mover), 
		transitions={'invalid':'End', 'valid':'Search', 'preempted':'End', 'invalid' : 'End', 'valid_no_object' : 'Search'}, 
		remapping={'move_pose_list':'sm_pose_base' , 'move_object_flag':'sm_object_flag'})
		
		#Wait for object positions
		smach.StateMachine.add('Search', Search(1), 
		transitions={'invalid':'Search', 'valid':'Move'}, 
		remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag', 'pose' : 'sm_pose_goal', 'pose_end': 'sm_pose_goal'})
		  
		#Move the robot to the specified goal
		smach.StateMachine.add('Move',Move(mover), 
		transitions={'invalid':'End', 'valid':'Lift', 'preempted':'End', 'invalid' : 'End', 'valid_no_object' : 'Lift'}, 
		remapping={'move_pose_list':'sm_pose_goal' , 'move_object_flag':'sm_object_flag'})

		
		#Lift or unlift the robot platform
		smach.StateMachine.add('Lift', Lift(1), transitions={'invalid':'Lift', 'valid':'getPose', 'preempted':'Lift', 'valid_unlift' : 'Init'}, remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
	  
		#Get pose from the user
		smach.StateMachine.add('getPose', WaitForMsgState("/user_pose", Pose, getPositionUser_V2, ['pose_user', 'pose_iteration', 'nb_robot'], ['pose_user', 'pose_iteration']), 
		transitions={'preempted' : 'getPose', 'aborted' : 'End', 'succeeded' : 'Move'},
		remapping={'pose_user':'sm_pose_goal' , 'pose_iteration' : 'sm_iteration_get_pose', 'nb_robot' : 'nb_robot'})

		#State for testing (?) that input goals for the robot if we do no visual search
		smach.StateMachine.add('CreateGoal', Back2Base(), 
		transitions={'invalid':'Init', 'valid':'Move', 'preempted':'Init'}, 
		remapping={'pose':'sm_pose_goal' , 'pose_base' : 'sm_pose_test'})     
		
		#LIFT BUG IN TWO NODE
		smach.StateMachine.add('Change_flag_lift', Change_variable(), transitions={'invalid':'Change_flag_lift', 'valid':'Lift', 'preempted':'Change_flag_lift'}, remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                  

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
