#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import rospy


#define state Lift
class Back2Base(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['valid','invalid','preempted'],
		input_keys=['pose_base' ],
		output_keys=['pose'])
		
	def execute(self, userdata):
		#rospy.loginfo('Executing state back to base for the target')
		#rospy.loginfo('Fixing the new arrival')
		
		#Copy the list
		userdata.pose=list(userdata.pose_base)
		
		return 'valid'