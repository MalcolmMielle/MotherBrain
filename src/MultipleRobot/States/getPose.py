#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import threading

import rospy


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
		print("It's not on the ground plane, the robot can't go there. Sorry, please give a new Pose")		
		return 'preempted'
	else:
		print("Good target")
		#return the position
		ud.pose_user[ud.pose_iteration].pose=msg
		ud.pose_iteration=ud.pose_iteration+1
		if ud.pose_iteration==ud.nb_robot:
			ud.pose_iteration=0
			return 'succeeded'
		return 'preempted'