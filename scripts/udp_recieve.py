#! /usr/bin/env python

import rospy
from std_msgs.msg import String
import socket
import referee_pb2

# import custom data message files
from referee.msg import debug_msg
from referee.msg import team_info
from referee.msg import point_2d


def udp_parser(referee_msg):
	rospy.loginfo('Received udp packet [{}]\n'.format(referee_msg.packet_timestamp))

	ros_msg     = debug_msg()
	blue_team   = team_info()
	yellow_team = team_info()
	ball_point  = point_2d()

	# blue team's details
	blue_team.name  = referee_msg.blue.name
	blue_team.score = referee_msg.blue.score

	# yellow team's details
	yellow_team.name  = referee_msg.yellow.name
	yellow_team.score = referee_msg.yellow.score

	# ball's position details
	ball_point.x = referee_msg.designated_position.x
	ball_point.y = referee_msg.designated_position.y

	# Decode all the remaining messages
	ros_msg.ts              = referee_msg.packet_timestamp
	ros_msg.stage           = int(referee_msg.stage)
	ros_msg.stage_time_left = referee_msg.stage_time_left
	ros_msg.command         = int(referee_msg.command)
	ros_msg.blue            = blue_team
	ros_msg.yellow          = yellow_team
	ros_msg.b_point         = ball_point

	# Return the packet
	return ros_msg


def client_data():
	# Initialise ros node and topic
	pub = rospy.Publisher('ref_data', debug_msg, queue_size=1000)
	rospy.init_node('referee', anonymous=True)

	host = '224.5.23.1'
	port = 10003
	max_bits = 1024

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Socket created'
	except socket.error, msg:
		print 'Failed to create socket. Error: ', str(msg[1])

	try:
		sock.bind((host, port))
		print 'Binding done!'
	except socket.error, msg:
		print 'Bind failed. Error: ', str(msg[1])

	print 'Waiting on port: ', port

	# receive data from client
	while not rospy.is_shutdown():
		# Read the message from referee 
		single_message = referee_pb2.SSL_Referee()
		data, addr = sock.recvfrom(max_bits)
		
		# Parse the udp data to protobuf message
		single_message.ParseFromString(data)
		
		# Convert protobuf message into ROS message type
		ros_msg = udp_parser(single_message)

		# Publish the message 
		pub.publish(ros_msg)

	sock.close()

if __name__=='__main__':
	try:
		client_data()
	except rospy.ROSInterruptException:
		pass
