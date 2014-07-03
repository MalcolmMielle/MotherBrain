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


#typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

class GoalMaker(object):
	
	def __init__(self, test, time):
		
		self.time_to_obj=time
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		if(test==False):
			rospy.loginfo("Waiting for move_base action server...")
			self.move_base.wait_for_server()
			
			rospy.loginfo("Connected to move base server")
			rospy.loginfo("Starting navigation")
        rospy.loginfo("The end")
		
		
		
	def move(self, posee, object_flag):
	
		goal = MoveBaseGoal()
		# Use the map frame to define goal poses
		goal.target_pose.header.frame_id = 'map'

		# Set the time stamp to "now"
		goal.target_pose.header.stamp = rospy.Time.now()

		# Set the goal there
		goal.target_pose.pose.position.x=posee.pose.position.x
		goal.target_pose.pose.position.z=posee.pose.position.y
		goal.target_pose.pose.position.z=0
		
		goal.target_pose.pose.orientation.x=posee.pose.orientation.x
		goal.target_pose.pose.orientation.y=posee.pose.orientation.y
		goal.target_pose.pose.orientation.z=posee.pose.orientation.z
		goal.target_pose.pose.orientation.w=posee.pose.orientation.w
		
		print
		print "this is the goal. Position : "+str(goal.target_pose.pose.position.x)+", "+str(goal.target_pose.pose.position.y)+", "+str(goal.target_pose.pose.position.z)+" Orientation : "+str(goal.target_pose.pose.orientation.x)+", "+str(goal.target_pose.pose.orientation.y)+", "+str(goal.target_pose.pose.orientation.z)+", "+str(goal.target_pose.pose.orientation.w)
		print 
		
		# Send the goal pose to the MoveBaseAction server
		self.move_base.send_goal(goal)

		# Allow 1 minute to get there
		finished_within_time = self.move_base.wait_for_result(rospy.Duration(self.time_to_obj)) 

		# If we don't get there in time, abort the goal
		if not finished_within_time:
			self.move_base.cancel_goal()
			rospy.loginfo("Timed out achieving goal")
			return 'preempted'
		else:
			# We made it!
			state = self.move_base.get_state()
		if state == GoalStatus.SUCCEEDED:
			rospy.loginfo("Goal succeeded! we have an object on us : %s" % str(object_flag) )
			if object_flag:
				return 'valid'
			else:
				return 'valid_no_object'
		else:
			return 'invalid'

	



# define state Bar
class Move(smach.State):
	def __init__(self, gm):
		smach.State.__init__(self,
		             input_keys=['move_pose', 'move_object_flag'],
                     outcomes=['invalid', 'valid', 'preempted', 'valid_no_object'])
		
		self.mover=gm
		self.pub_new=rospy.Publisher('pose_final', PoseStamped, queue_size=1)
        
	def execute(self, userdata):
#		rospy.loginfo('Executing move robot state')

		#Move and wait
		result=self.mover.move(userdata.move_pose, userdata.move_object_flag)
		
		#Publish the new pose. I don't really know why I'm doing that
		self.pub_new.publish(userdata.move_pose)
		
		#Return the result
		if(userdata.move_object_flag==False): #It means you are not lifting an object
			return result
		else:
			return result #TODO