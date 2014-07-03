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
	pose_base = PoseStamped()
	pose_base.pose.position.x=1000
	rospy.loginfo("Going in ;)")
	mover=GoalMaker(True, 1) #set at true for testing !
	rospy.loginfo("DOne")
	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	sm.userdata.sm_pose_goal = pose #Don't know how to declare a message...
	sm.userdata.sm_object_flag = False
	sm.userdata.sm_pose_base=pose_base
	# Open the container
	with sm: 
		# Add states to the container
		
		                  
		                  
		smach.StateMachine.add('Lift', Lift(), 
		transitions={'invalid':'Lift_bug', 'valid':'Lift', 'preempted':'Lift_bug', 'valid_unlift' : 'Lift'}, 
		remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                  
		                  
		smach.StateMachine.add('Lift_bug', Lift_bug(), 
		transitions={'invalid':'Lift_bug', 'valid':'Lift', 'preempted':'Lift_bug'},
		remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                      
		                  

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
