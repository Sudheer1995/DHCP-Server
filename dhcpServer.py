#!/usr/bin/python
import math
import socket
import operator
from thread import *

class dhcpServer:
	''' functionalities of dhcp Server '''
	def __init__(self):
		''' initialize the port and open a new socket for connection '''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 6000
		self.hostname = socket.gethostname()
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1000)
		self.labs = {}
		self.macs = {}
		# information to be sent back
		self.Ips = {}
		self.Subnet = {}
		self.netAddress = {}
		self.broadAddress = {}
		self.DNSGateway  = {}
		self.setData()
		self.allocateIpsToLabs()
	
	def setData(self):
		
		with open('subnets.conf','r') as subnet_file:
		
			line_number = 1

			for line in subnet_file:
				if line_number == 1:
					IpDetails = line.split('/')
					self.startIp = IpDetails[0]
					self.numberOfIps = 2**(32 - int(IpDetails[1])) - 2				
				elif line_number == 2:
					self.numberOfLabs = int(line)
				elif line_number >= 3 and line_number <= 3 + self.numberOfLabs - 1:
					labDetails = line.split(':')
					self.labs[labDetails[0]] = int(labDetails[1])
				else:
					macDetails = line.split()
					self.macs[macDetails[0]] = macDetails[1]
				line_number += 1

	def allocateIpsToLabs(self):

		labs = sorted(self.labs.items(), key=operator.itemgetter(0))
		
		currentIp = self.startIp

		for lab in labs:
			self.Ips[lab[0]] = []
			
			# Subnet mask
			hosts = int(math.ceil(math.log(lab[1], 2)))
			bits = 32 - hosts
			self.Subnet[lab[0]] = bits
			
			for i in range(0, 2**hosts):
				if i == 1:
					# Network Address
					self.Ips[lab[0]].append([currentIp, 1])
				else:
					# Host Address
					self.Ips[lab[0]].append([currentIp, 0])
					currentIpParts = currentIp.split('.')
					currentIpParts = [int(i) for i in currentIpParts]
					for j in range(3, -1, -1):
						currentIpParts[j] += 1
						if currentIpParts[j] <= 255:
							break
						else:
							currentIpParts[j] = 0
					currentIp = '.'.join(str(part) for part in currentIpParts)

			# Network Address
			networkAddress = self.Ips[lab[0]]
			self.netAddress[lab[0]] = networkAddress[0][0]
		
			# Broadcast Address
			BroadCast = self.Ips[lab[0]]
			self.broadAddress[lab[0]] = BroadCast[len(BroadCast)-1][0]
		
			# Same DNS, Gateway Address
			DNSGateWay = self.Ips[lab[0]]
			self.DNSGateway[lab[0]] = DNSGateWay[int(len(DNSGateWay)/2)][0]
 
	def dhcpDiscover(self, conn):
		''' receive the request from client for connection '''
		mac_address = conn.recv(17)
		lab = self.macs[mac_address]
		if len(self.Ips[lab]) != 0:
			i = 0
			while self.Ips[lab][i][1] != 0:
				i += 1

			ipToAssign = self.Ips[lab][i][0]
			subnet = self.Subnet[lab]
			ipToAssign = '/'.join([str(ipToAssign), str(subnet)])
		self.dhcpOffer(ipToAssign, lab, conn)

	def dhcpOffer(self, ip, lab, conn):
		''' send the ipAddress assigned to the client '''
		# Send Ip Address
		Ack = False
		while not Ack:
			conn.send(ip)
			Ack = bool(conn.recv(10))
		# Send Network Address
		Ack = False
		while not Ack:
			conn.send(str(self.netAddress[lab]))
			Ack = bool(conn.recv(10))
		# Send broadAddress
		Ack = False
		while not Ack:	
			conn.send(str(self.broadAddress[lab]))
			Ack = bool(conn.recv(10))
		# Send DNS & Gateway Address
		Ack = False
		while not Ack:
			conn.send(str(self.DNSGateway[lab]))
			Ack = bool(conn.recv(10))

		self.dhcpRequest(ip, lab, conn)

	def dhcpRequest(self, ip, lab, conn):
		''' receive the IP addresses sent by dhcpOffer() from 
			client to verify proper addresses is received '''
		assignedIp = conn.recv(32)

		if assignedIp == ip:
			self.dhcpAck(1, lab, ip, conn)

		else:
			self.dhcpAck(0, lab, ip, conn)

	def dhcpAck(self, ack, lab, ip, conn):
		''' send an acknowledgement to client if an dhcpRequest() 
			verification is passed otherwise send an not an acknowledgement '''
		if ack:
			conn.send('ACK')
			for i in range(0, len(self.Ips[lab])):
				if self.Ips[lab][i][0] == ip:
					break
			self.Ips[lab][i][1] = 1

		else:
			conn.send('NACK')
			self.dhcpDiscover(conn)


if __name__ == "__main__":
	
	server = dhcpServer()

	while True:
		conn, addr = server.socket.accept()
		start_new_thread(server.dhcpDiscover,(conn,))	