import numpy
import math

class Request:
	global request
	request = 0
	inCoreQueue = False
	totalServiceTime = 0
	remainingServiceTime = 0
	clientId = 0
	threadId = 0
	def __init__(self, time):
		self.requestId = request+1
		self.timestamp = time
		global request
		request +=1
		
	def setTimeOutDistribution(self, dis = "exponential" , a = 50, b = 1):
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
			
		
	def getTimeOut(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
			
	def setArrivalTimeDistribution(self, dis = "exponential" , a = 50, b = 1):
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
	
	def getArrivalTime(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
		
	def setServiceTimeDistribution(self, dis = "exponential" , a = 50, b = 1):
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
		
	def getServiceTime(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
		
	def setInCoreQueue(self, queue):
		self.inCoreQueue = queue
		
	def getInCoreQueue(self):
		return self.inCoreQueue
        
