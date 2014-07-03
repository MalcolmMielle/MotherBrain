#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import sys

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from motherbrain.srv import *

"""class ServiceVisu(object):
	def __init__(self, name):
		self.serviceGotObject = rospy.ServiceProxy(name, getobject)
"""

# define state Foo
class Search(smach.State):
	def __init__(self, name):
		smach.State.__init__(self, outcomes=['invalid', 'valid'],
		#input_keys=['search_services'],
		output_keys=['searched_pose'])
		
		self.serviceGotObject = rospy.ServiceProxy(name, getobject)
		

	def execute(self, userdata):
#		rospy.loginfo('Executing state Searching for the target')
		
		#ask for the service
		rep=getobject
		#Handle unavailable service
		try:
			rep=self.serviceGotObject(True)
		except Exception, e:
			print( "<p>Error: %s</p>" % str(e) )
			rep.gotObject=True #JUST FOR TESTING TODO Change it to false
			rep.pose=PoseStamped

		print( "Asked if a model was found with rep : %s" % str(rep.gotObject) )
		if rep.gotObject==True:
			search_pose=rep.pose
			return 'valid'
		else:
			return 'invalid'
	    
		
		

		
