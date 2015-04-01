import numpy
import math

class Client:
	maxNoOfClients = 60
	currentNoOfClients = 0
	#class constructor 
	def __init__(self):
		Client.currentNoOfClients += 1
		self.clientId = Client.currentNoOfClients
		self.setIsThinking(False)
	#setting parameters and type of distribution for think time	
	def setThinkTimeDistribution(self, dis = "uniform" , a = 5, b = 10):
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
	#this will give the think time	
	def getThinkTimeValue(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
	#to set whether client is thinking or not.
	def setIsThinking(self, value):
		self.isThinking = value
	#to get status of client	
	def getIsThinking(self):
		return self.isThinking
		