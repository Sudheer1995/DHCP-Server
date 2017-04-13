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
		# recieve Ip Address	
		assignedIp = ''	
		while not assignedIp:
			assignedIp = self.clientSocket.recv(32)
			self.clientSocket.send(str(True))
		self.ip =  assignedIp
		# recieve Network Address
		assignedNetworkAddress = ''
		while not assignedNetworkAddress:
			assignedNetworkAddress = self.clientSocket.recv(32)
			self.clientSocket.send(str(True))
		self.networkAddress = assignedNetworkAddress
		# recieve BroadCast Address
		assignedBroadCastAddress = ''
		while not assignedBroadCastAddress:
			assignedBroadCastAddress = self.clientSocket.recv(32)
			self.clientSocket.send(str(True))
		self.broadcastAddress = assignedBroadCastAddress
		# recieve DNS & Gateway Address
		assignedDNSGateway = ''
		while not assignedDNSGateway:
			assignedDNSGateway = self.clientSocket.recv(32)
			self.clientSocket.send(str(True))
		self.DNS = assignedDNSGateway
		self.gateWay = assignedDNSGateway
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
	print client.networkAddress
	print client.broadcastAddress
	print client.DNS
	print client.gateWay