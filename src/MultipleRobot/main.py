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
from States.back2Base import *
from States.util import *




def main():
	rospy.init_node('MotherBrain')
	
	#Service, publisher subscribers definition
	pose = PoseStamped()
	pose.pose.orientation.w=1
	pose.pose.position.x=1
	pose_base = PoseStamped()
	pose_base.pose.orientation.w=1
	mover=GoalMaker(False, 60) #set at true for testing !

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	#sm.userdata.rospy.Subscriber("chatter", String, callback)
	sm.userdata.sm_pose_goal = list() #Don't know how to declare a message...
	sm.userdata.sm_pose_base = list()
	sm.userdata.sm_object_flag = False

	# Open the container
	with sm:
		# Add states to the container
		smach.StateMachine.add('Search', Search('robot1/getObject', 'robot2/getObject'), 
		transitions={'invalid':'Search', 'valid':'Move'},
		remapping={'searched_pose':'sm_pose_goal_robot1'})
		
		
		smach.StateMachine.add('Move', Move(mover), 
		transitions={'valid_no_object':'Lift', 'invalid':'Lift_bug', 'valid':'Lift', 'preempted':'Lift_bug'},
		remapping={'move_pose':'sm_pose_goal' , 'move_object_flag':'sm_object_flag'})
		
		
		#Change transitions for the return to base
		smach.StateMachine.add('Lift', Lift(), 
		transitions={'invalid':'Lift_bug', 'valid':'MoveUser', 'preempted':'Lift_bug', 'valid_unlift':'Back2Base'}, 
		remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                  
		                  
		smach.StateMachine.add('Lift_bug', Lift_bug(), 
		transitions={'invalid':'Lift_bug', 'valid':'Back2Base', 'preempted':'Lift_bug'},
		remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                      
		                      
		smach.StateMachine.add('Back2Base', Back2Base(), 
		transitions={'invalid':'Back2Base', 'valid':'Move_Base', 'preempted':'Back2Base'}, 
		remapping={'pose':'sm_pose_goal' , 'pose_base' : 'sm_pose_base'})
		
		#Change End to Search for more than one turn
		smach.StateMachine.add('Move_Base', Move(mover), 
		transitions={'valid_no_object':'End', 'invalid':'Lift_bug', 'valid':'Lift_bug', 'preempted':'Lift_bug'},
		remapping={'move_pose':'sm_pose_goal' , 'move_object_flag':'sm_object_flag'})
		                       
#		smach.StateMachine.add('MoveUser', MonitorState2("/user_pose", Pose, getPositionUser) , transitions={'invalid':'MoveUser', 'valid':'Move', 'preempted':'MoveUser'}, remapping={'pose_user':'sm_pose_goal'})

		smach.StateMachine.add('MoveUser', WaitForMsgState("/user_pose", Pose, getPositionUser_V2, ['pose_user'], ['pose_user']), 
		transitions={'preempted' : 'MoveUser', 'aborted' : 'MoveUser', 'succeeded' : 'Move'},
		remapping={'pose_user':'sm_pose_goal'})
		                     

	# Create and start the introspection server
#	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
#	sis.start()

	# Execute the state machine
	outcome = sm.execute()

	# Wait for ctrl-c to stop the application
#	rospy.spin()
#	sis.stop()


if __name__ == '__main__':
    main()
