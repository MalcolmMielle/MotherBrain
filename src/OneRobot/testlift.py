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




def main():
	rospy.init_node('MotherBrain')
	
	pose = PoseStamped()

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['End'])
	#sm.userdata.sm_counter = 0
	sm.userdata.sm_pose = pose #Don't know how to declare a message...
	sm.userdata.sm_object_flag=False

	# Open the container
	with sm:
		# Add states to the container
		
		smach.StateMachine.add('Lift', Lift(), 
		                      transitions={'invalid':'Lift', 'valid':'Lift', 'preempted':'Lift', 'valid_unlift' : 'Lift'},
		                      remapping={'flag' : 'sm_object_flag', 'end_object_flag':'sm_object_flag'})
		                       

	# Create and start the introspection server


	# Execute the state machine
	outcome = sm.execute()




if __name__ == '__main__':
    main()
