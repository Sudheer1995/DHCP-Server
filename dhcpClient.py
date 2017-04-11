#!/usr/bin/python
import socket

class dhcpClient:
	''' client requests methods for a connection to dhcp Server '''
	def __init__(self):
		''' initilize the port and open a socket for other end of
			communication requesting a connection dhcp Server '''
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientPort = 6000
	 	self.hostname = socket.gethostname()
		self.clientSocket.connect((self.hostname, self.clientPort))
	
	def clientDiscover():
		''' send the request for dhcp server for a connection '''

	def clientOffer():
		''' take the IP address sent by the dhcp Server '''

	def clientRequest():
		''' send back the IP address sent by dhcp Server
			for verification of proper communication channel '''
	def clientAck():
		''' receive the acknowledgment sent by dhcp Server '''

if __name__ == "__main__":
	
	client = dhcpClient()