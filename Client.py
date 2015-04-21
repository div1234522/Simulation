import numpy
import math

class Client:
	maxNoOfClients = 60
	currentNoOfClients = 0
	thinktime_c = 0
	
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
			self.thinktime_c = math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
			self.thinktime_c = math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			self.value = a
			self.thinktime_c = self.value
			
	#this will give the think time	
	def getThinkTimeValue(self):
		return self.thinktime_c
		
	#to set whether client is thinking or not.
	def setIsThinking(self, value):
		self.isThinking = value
		
	#to get status of client	
	def getIsThinking(self):
		return self.isThinking
		