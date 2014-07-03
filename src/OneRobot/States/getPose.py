#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import threading

import rospy

#Overload the monitor to have input / output
class MonitorState2(smach_ros.MonitorState):
	def __init__(self, topic, msg_type, cond_cb, max_checks=-1):
		smach.State.__init__(self, outcomes=['valid', 'invalid', 'preempted'], output_keys=['pose_user'])

		self._topic = topic 
		self._msg_type = msg_type 
		self._cond_cb = cond_cb 
		self._max_checks = max_checks 
		self._n_checks = 0 

		self._trigger_cond = threading.Condition()
		
		print("DEFINTION")
		
		
	def execute(self, ud):
		self._n_checks = 0
		print 'wat get in'
		self._sub = rospy.Subscriber(self._topic, self._msg_type, self._cb, callback_args=ud)
		print ' and get out'
		self._trigger_cond.acquire()
		print ' and get acquired'
		self._trigger_cond.wait()
		print ' and get waited'
		self._trigger_cond.release()
		print ' and get released'

		self._sub.unregister()
		print ' unregistered'

		if self.preempt_requested():
			self.service_preempt()
			print 'wat'
			return 'preempted'

		if self._max_checks > 0 and self._n_checks >= self._max_checks:
			print 'valid'
			return 'valid'
		print 'invalid'
		return 'invalid'





def getPositionUser(ud, msg): #Userdata and message
	print('get in monitor')
	print "this is the message. Position : "+str(msg.position.x)+", "+str(msg.position.y)+", "+str(msg.position.z)+" Orientation : "+str(msg.orientation.x)+", "+str(msg.orientation.y)+", "+str(msg.orientation.z)+", "+str(msg.orientation.w)
	
	#We want a plane and orientation only around the z axis.
	"""Quaternion : 
	q[0]=cos(r/2)
	q[1]=cos(r/2)*x
	q[2]=cos(r/2)*y
	q[3]=cos(r/2)*z
	
	So we 0 out the y and x"""
	#print str(ud.pose_user.position.x)
	
	if msg.position.z != 0.0 or msg.orientation.y != 0 or msg.orientation.z != 0:
		print("It's not on the ground plane, the robot can't go there. Sorry")		
		return 'invalid'
	else:
		print("Good")
		
		#return the position
		ud.pose_user=msg
		
		return 'valid'
		
		
		
def getPositionUser_V2(msg, ud): #Userdata and message
	#print('get in monitor')
	print "this is the message. Position : "+str(msg.position.x)+", "+str(msg.position.y)+", "+str(msg.position.z)+" Orientation : "+str(msg.orientation.x)+", "+str(msg.orientation.y)+", "+str(msg.orientation.z)+", "+str(msg.orientation.w)
	
	#We want a plane and orientation only around the z axis.
	"""Quaternion : 
	q[0]=cos(r/2)
	q[1]=cos(r/2)*x
	q[2]=cos(r/2)*y
	q[3]=cos(r/2)*z
	
	So we 0 out the y and x"""
	#print str(ud.pose_user.position.x)
	
	if msg.position.z != 0.0 or msg.orientation.y != 0 or msg.orientation.z != 0:
		print("It's not on the ground plane, the robot can't go there. Sorry")		
		return False
	else:
		print("Good target")
		
		#return the position
		ud.pose_user.pose=msg
		
		return True