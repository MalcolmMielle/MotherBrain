#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import rospy

from motherbrain.srv import *


#define state Lift
class Lift(smach.State):
	def __init__(self, nbRobot):
		smach.State.__init__(self, outcomes=['valid','invalid','preempted','valid_unlift'],
		input_keys=['flag', 'nbRobot'],
		output_keys=['end_object_flag'])
		
		rospy.loginfo('Waiting for the service in lift')
		self.serviceLift = list()
		self.nbRobot=nbRobot
		try:
			i=0
			if nbRobot>1:
				while i<nbRobot:
					name='robot'+str(i)+'/lifting_service'
					rospy.wait_for_service(name)
					i=i+1
					self.serviceLift.append(rospy.ServiceProxy(name, lifting) )
			else:
				name='/lifting_service'
				rospy.wait_for_service(name)
				i=i+1
				self.serviceLift.append(rospy.ServiceProxy(name, lifting) )
		except rospy.ServiceException, e:
				print "Service call failed: %s"%e
		
	def execute(self, userdata):
		rospy.loginfo('Executing state Lifting for the target')
		
		flag=1
		
		for elm in self.serviceLift:
			print 'flag '+str(flag)
			if userdata.flag == True:
				#Do processing to unlift
				rospy.loginfo('Unlift')
				try:
					rep=elm('down')
				except rospy.ServiceException, e:
					print "Service call failed: %s"%e
				if(rep.answer==True) and flag==self.nbRobot:
					userdata.end_object_flag=False
					print('The object is now UN-lifted')
					return 'valid_unlift'
				elif (rep.answer==True) and flag<self.nbRobot:
					flag=flag+1
				elif (rep.answer==True) and flag>self.nbRobot:
					return 'invalid'
				else:
					return 'invalid'
				
			else:
				#Do processing to lift
				rospy.loginfo('Lift')
				try:
					rep=elm('up')
				except rospy.ServiceException, e:
					print "Service call failed: %s"%e
				if(rep.answer==True) and flag==self.nbRobot:
					userdata.end_object_flag=True
					print('The object is now lifted')
					return 'valid'
				elif (rep.answer==True) and flag<self.nbRobot:
					flag=flag+1
				elif (rep.answer==True) and flag>self.nbRobot:
					return 'invalid'
				else:
					return 'invalid'
			
		return 'invalid'
#		rospy.loginfo('done. We have : ' + str(userdata.flag) )
		
		
		
		
		
#define state unLift must be followed by lift state
class Change_variable(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['valid','invalid','preempted'],
		input_keys=['flag'],
		output_keys=['end_object_flag'])
		
	def execute(self, userdata):
		#rospy.loginfo('Executing state Lifting for the target')
		
		#Do processing to unlift
		userdata.end_object_flag=True
		print('The object is now lifted to prevent errors. If no object is on the robot please do not consider this message')
			
		rospy.loginfo('done. We have : ' + str(userdata.flag) )
		
		return 'valid'
		
		