#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import rospy

from motherbrain.srv import *


#define state Lift
class Lift(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['valid','invalid','preempted','valid_unlift'],
		input_keys=['flag'],
		output_keys=['end_object_flag'])
		
		rospy.loginfo('Waiting for the service in lift')
		try:
			rospy.wait_for_service('lifting_service')
		except rospy.ServiceException, e:
				print "Service call failed: %s"%e
		self.serviceLift = rospy.ServiceProxy('lifting_service', lifting)
		
	def execute(self, userdata):
		rospy.loginfo('Executing state Lifting for the target')
		
		if userdata.flag == True:
			#Do processing to unlift
			rospy.loginfo('Unlift')
			try:
				rep=self.serviceLift('down')
			except rospy.ServiceException, e:
				print "Service call failed: %s"%e
			if(rep.answer==True):
				userdata.end_object_flag=False
				print('The object is now UN-lifted')
				return 'valid_unlift'
			else:
				return 'invalid'
			
		else:
			#Do processing to lift
			rospy.loginfo('Lift')
			try:
				rep=self.serviceLift('up')
			except rospy.ServiceException, e:
				print "Service call failed: %s"%e
			if(rep.answer==True):
				userdata.end_object_flag=True
				print('The object is now lifted')
				return 'valid'
			else:
				return 'invalid'
			
#		rospy.loginfo('done. We have : ' + str(userdata.flag) )
		
		
		
		
		
#define state Lift
class Lift_bug(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['valid','invalid','preempted'],
		input_keys=['flag'],
		output_keys=['end_object_flag'])
		
	def execute(self, userdata):
		#rospy.loginfo('Executing state Lifting for the target')
		
		#Do processing to unlift
		userdata.end_object_flag=False
		print('The object is now UN-lifted')
			
		rospy.loginfo('done. We have : ' + str(userdata.flag) )
		
		return 'valid'
		
		