import numpy
import math

class Client:
	maxNoOfClients = 5
	currentNoOfClients = 0
	
	def __init__(self):
		Client.currentNoOfClients += 1
		self.clientId = Client.currentNoOfClients
		self.setIsThinking(False)
		
	def setThinkTimeDistribution(self, dis = "uniform" , a = 5, b = 10):
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
		
	def getThinkTimeValue(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
		
	def setIsThinking(self, value):
		self.isThinking = value
		
	def getIsThinking(self):
		return self.isThinking
		