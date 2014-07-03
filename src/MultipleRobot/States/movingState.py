#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros

import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import *
from geometry_msgs.msg import *
from itertools import *


def printPoseStamped(elm):
	print " Position : "+str(elm.pose.position.x)+", "+str(elm.pose.position.y)+", "+str(elm.pose.position.z)+" Orientation : "+str(elm.pose.orientation.x)+", "+str(elm.pose.orientation.y)+", "+str(elm.pose.orientation.z)+", "+str(elm.pose.orientation.w)
	print 

	
#Goalmove base and PoseStamped
def copyGoal(goal, posee):
	# Use the map frame to define goal poses
	goal.target_pose.header.frame_id = 'map'

	# Set the time stamp to "now"
	goal.target_pose.header.stamp = rospy.Time.now()
	print 'posee',
	printPoseStamped(posee)
	print 'goal',
	printPoseStamped(goal.target_pose)
	# Set the goal there
	goal.target_pose.pose.position.x=posee.pose.position.x
	goal.target_pose.pose.position.y=posee.pose.position.y
	goal.target_pose.pose.position.z=0
	
	goal.target_pose.pose.orientation.x=posee.pose.orientation.x
	goal.target_pose.pose.orientation.y=posee.pose.orientation.y
	goal.target_pose.pose.orientation.z=posee.pose.orientation.z
	goal.target_pose.pose.orientation.w=posee.pose.orientation.w
	
#typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

class GoalMaker(object):
	
	#test define if we just want to test the class itself and thus we don't want to connect, just test the function : True -> Testing, False -> NotTesting (connection done)
	def __init__(self, test, nbRobot, time):
		
		self.ndRobot=nbRobot
		self.time_to_obj=time
		self.move_base = list()
		i=0
		while i < nbRobot:
			name='robot'+str(i)+'/move_base'
			print 'connecting to : ' + str(name)
			self.move_base.append(actionlib.SimpleActionClient(name, MoveBaseAction))
			if(test==False):
				rospy.loginfo("Waiting for move_base action server...")
				self.move_base[i].wait_for_server()
				
				rospy.loginfo("Connected to move base server")
				rospy.loginfo("Starting navigation")
			i=i+1
		rospy.loginfo("The end")
		
	
		
	def move(self, pose_list, object_flag):
		
		print 'size of both ' + str(len(pose_list))+' '+str(len(self.move_base))
		try:
			if len(pose_list) != len(self.move_base):
				raise Exception("pose number different than robot number")
			else:
				for elm_pose, elm_goal in izip ( pose_list, self.move_base ):
					
					printPoseStamped(elm_pose)
					
					goal = MoveBaseGoal()
					
					copyGoal(goal, elm_pose)
					
					print 'we have move_base : ' + str(elm_goal)
					print "this is the goal. Position : "+str(goal.target_pose.pose.position.x)+", "+str(goal.target_pose.pose.position.y)+", "+str(goal.target_pose.pose.position.z)+" Orientation : "+str(goal.target_pose.pose.orientation.x)+", "+str(goal.target_pose.pose.orientation.y)+", "+str(goal.target_pose.pose.orientation.z)+", "+str(goal.target_pose.pose.orientation.w)
					print 
					
					# Send the goal pose to the MoveBaseAction server
					print 'sending the goal'
					elm_goal.send_goal(goal)

					# Allow 1 minute to get there
					print 'wait for result for : '+str(self.time_to_obj)
					finished_within_time = elm_goal.wait_for_result(rospy.Duration(self.time_to_obj)) 

					# If we don't get there in time, abort the goal
					if not finished_within_time:
						elm_goal.cancel_goal()
						rospy.loginfo("Timed out achieving goal")
						return 'preempted'
					else:
						# We made it!
						state = elm_goal.get_state()
					if state == GoalStatus.SUCCEEDED:
						rospy.loginfo("Goal succeeded! we have an object on us : %s" % str(object_flag) )
					else:
						rospy.loginfo("Goal not succeeded :( ! we have an object on us : %s" % str(object_flag) )
						return 'invalid'
						
				if object_flag:
					return 'valid'
				else:
					return 'valid_no_object'
		except Exception, e:
				print "Robot move: %s , "%e

	



# define state Bar
class Move(smach.State):
	def __init__(self, gm):
		smach.State.__init__(self,
		             input_keys=['move_pose_list', 'move_object_flag'],
                     outcomes=['invalid', 'valid', 'preempted', 'valid_no_object'])
		
		self.mover=gm
		self.pub_new=rospy.Publisher('pose_final', PoseStamped, queue_size=1)
        
	def execute(self, userdata):
#		rospy.loginfo('Executing move robot state')

		#Move and wait
		
		result=self.mover.move(userdata.move_pose_list, userdata.move_object_flag)
		
		#Publish the new pose. I don't really know why I'm doing that
		#self.pub_new.publish(userdata.move_pose_list)
		
		#Return the result
		return result
