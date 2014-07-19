#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import sys

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
from motherbrain.srv import *

"""class ServiceVisu(object):
	def __init__(self, name):
		self.serviceGotObject = rospy.ServiceProxy(name, getobject)
"""

# define state Foo
class Search(smach.State):
	
	def reinit(self):
		i=0
		while i<self.nbRobot:
			self.flagrobot[i]=False
			self.pose_robot[i]=PoseStamped()
			i +=1
		self.all_search_complete=False

	
	def poseEqual(self, pose1, pose2):
		if(pose1.position.x==pose2.position.x and pose1.position.y==pose2.position.y and pose1.position.z==pose2.position.z and pose1.orientation.x==pose2.orientation.x and pose1.orientation.y==pose2.orientation.y and pose1.orientation.z==pose2.orientation.z and pose1.orientation.w==pose2.orientation.w):
			return True
		else:
			return False
			
	def checkAllRobotFlag(self):
		for elm in self.flagrobot:
			if elm==False:
				return False
		return True
		
	def isvalidTarget(self, pose):
		#TODO
		for elm in self.pose_robot:
			if self.poseEqual(elm.pose, pose.pose):
				return False
		return True
	
	def check(self, rep):
		print 'received'
		#program cool stuff
		#TODO multiple robot

		if(self.nbRobot==1):
			self.pose_robot[0]=rep.pose
			self.flagrobot[0]=True
			self.all_search_complete=True
			return sentobjectResponse(False)
			
		#TODO
		else:
			try:
				if rep.robot_id<self.nbRobot and rep.robot_id>=0:
					if self.isvalidTarget(rep.pose)==False :
						return sentobjectResponse(True)
					else :
						self.pose_robot[rep.robot_id]=rep.pose #TODO
						self.flagrobot[rep.robot_id]=True
						if self.checkAllRobotFlag():
							self.all_search_complete=True
						return sentobjectResponse(False)
				else:
					raise Exception("Robot ID is not in the good limit")
			except Exception, e:
				print "Robot ID fail: %s , it should be between 0 and %s "%e %self.nbRobot
			
			
			
	
	
	def __init__(self, name, ndRobot):
		smach.State.__init__(self, outcomes=['invalid', 'valid'],
		input_keys=['end_object_flag', 'pose'],
		output_keys=['flag', 'pose_end'])
		
		rospy.loginfo('Creating services client of search')
		try:
			if ndRobot>2:
				raise Exception("To many robot")
			if ndRobot<0:
				raise Exception("Not enough Robots")
			if len(name) != ndRobot:
				raise Exception("Not the same number of robot and services")
		except Exception, e:
				print "Number of robot fail: %s"%e
				print "going for the default value of 1 and service sentobject"
				ndRobot=1
				name=['sentobject']
				
		
		self.service =rospy.Service('sentobject', sentobject, self.check)
		self.pose_robot=list()
		self.flagrobot=list()
		#Initialise flag robot list
		i=0
		while i<ndRobot:
			self.flagrobot.append(False)
			self.pose_robot.append(PoseStamped() )
			i +=1
		self.nbRobot=ndRobot;
		self.all_search_complete=False
		self.pub = rospy.Publisher('search', Bool, queue_size=1)
		
		
	def printPose(self):
		for elm in self.pose_robot:
			print 'pose : ' + str(elm.pose.position.x) + ' '+ str(elm.pose.position.y) + ' '+ str(elm.pose.position.z) +' orientation ' + str(elm.pose.orientation.x)+ ' '+ str(elm.pose.orientation.y)+ ' '+ str(elm.pose.orientation.z)+ ' '+ str(elm.pose.orientation.w)
		
	def printFlags(self):
		for elm in self.flagrobot:
			print 'flags : ' + str(elm),
		print
		

	def execute(self, userdata):
		rospy.loginfo('Executing state Searching for the target')
		print '\n'+'SEARCH GIVE US ' + str(self.all_search_complete) +' and '+str(self.nbRobot)+ '\n'

		if self.all_search_complete==False:
			 pub.publish(True)
		
		self.printPose()
		self.printFlags()
		print 'Thus '+str(self.checkAllRobotFlag() )
		
		#if self.isvalidTarget(self.pose_robot[0])==False:
		#	print 'bouyaka '
			#exit(0)
		
		
		if self.all_search_complete==True:
			#self.reinit()
			pub.publish(False)
			self.all_search_complete=False
			return 'valid'
		else:
			return 'invalid'
		
		#rospy.spin() 
		"""Don't need it : The final addition, rospy.spin() simply keeps your node from exiting 
		until the node has been shutdown. Unlike roscpp, rospy.spin() does not 
		effect the subscriber callback functions, it simply puts the node to 
		sleep until it has been shut down. In rospy, each subscriber has its 
		
		own thread which handles its callback functions automatically."""
		#rospy.spin()
