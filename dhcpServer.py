#!/usr/bin/python
import socket

class dhcpServer:
	''' functionalities of dhcp Server '''
	def __init__(self):
		''' initialize the port and open a new socket for connection '''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 6000
		self.hostname = socket.gethostname()
		self.socket.bind(self.hostname, self.port)
		self.socket.listen(5)

	def dhcpDiscover(self):
		''' receive the request from client for connection '''

	def dhcpOffer(self):
		''' process the request from client and assign 
			a IP address from the pool of addresses '''

	def dhcpRequest(self):
		''' receive the IP addresses sent by dhcpOffer() from 
			client to verify proper addresses is received '''

	def dhcpAck(self):
		''' send an acknowledgement to client if an dhcpRequest() 
			verification is passed otherwise send an not an acknowledgement '''

if __name__ == "__main__":
	
	server = dhcpServer()