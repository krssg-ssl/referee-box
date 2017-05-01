#! /usr/bin/env python

import rospy
from std_msgs.msg import String
import socket
import referee_pb2

def client_data():
	pub = rospy.Publisher('ref_data', , queue_size=100)
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
	except socket.error, msg:
		print 'Bind failed. Error: ', str(msg[1])

	print 'Waiting on port: ', port

	# receive data from client
	while not rospy.is_shutdown():
		single_message = referee_pb2.SSL_Referee()
		data, addr = sock.recvfrom(max_bits)
		
		# decode the message and publish over topic
		pub.publish()

	sock.close()

if __name__=='__main__':
	try:
		client_data()
	except rospy.ROSInterruptException:
		pass
