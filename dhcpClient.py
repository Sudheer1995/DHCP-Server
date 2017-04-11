#!/usr/bin/python
import socket

class dhcpClient:
	''' client requests methods for a connection to dhcp Server '''
	def __init__(self, mac):
		''' initilize the port and open a socket for other end of
			communication requesting a connection dhcp Server '''
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientPort = 6000
	 	self.hostname = socket.gethostname()
		self.clientSocket.connect((self.hostname, self.clientPort))
		self.mac = mac
	
	def clientDiscover(self):
		''' send the request for dhcp server for a connection '''
		self.clientSocket.send(self.mac)
		self.clientOffer()

	def clientOffer(self):
		''' take the IP address sent by the dhcp Server '''
		assignedIp = self.clientSocket.recv(32)
		self.clientRequest(assignedIp)

	def clientRequest(self, ip):
		''' send back the IP address sent by dhcp Server
			for verification of proper communication channel '''
		self.clientSocket.send(ip)
		self.clientAck(ip)

	def clientAck(self, ip):
		''' receive the acknowledgment sent by dhcp Server '''
		ack = self.clientSocket.recv(4)
		if ack:
			self.ip = ip
		else:
			self.clientDiscover()


if __name__ == "__main__":
	
	mac = str(raw_input())
	client = dhcpClient(mac)
	client.clientDiscover()
	print client.ip