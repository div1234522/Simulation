import numpy #For distributions
import math #For ceiling function

class Request:
	global request #Stores requestID count
	request = 0
	timestamp = 0
	inCoreQueue = False
	totalServiceTime = 0
	remainingServiceTime = 0
	clientId = 0
	threadId = 0
	def __init__(self): #Class constructor
		self.requestId = request+1
		global request
		request +=1
	
	def zero(self):
		global request
		request = 0
		
	def setTimeOutDistribution(self, dis = "exponential" , a = 50, b = 1): #Set type of distribution
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
			
		
	def getTimeOut(self): #Get value according to distribution
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
			
	def setArrivalTimeDistribution(self, dis = "exponential" , a = 50, b = 1): #Set type of distribution
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
	
	def getArrivalTime(self): #Get value according to distribution
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
		
	def setServiceTimeDistribution(self, dis = "exponential" , a = 50, b = 1): #Set type of distribution
		self.dis_type = dis
		if self.dis_type == 'exponential':
			self.mean = a
		if self.dis_type == 'uniform':
			self.low = a
			self.high = b
		if self.dis_type == 'constant':
			self.value = a
		
	def getServiceTime(self): #Get value according to distribution
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
		if self.dis_type == 'uniform':
			return math.ceil(numpy.random.uniform(self.low, self.high))
		if self.dis_type == 'constant':
			return self.value
		
	def setInCoreQueue(self, queue): #Set whether the request is in core queue or not
		self.inCoreQueue = queue
		
	def getInCoreQueue(self): #Get the status of request to calculate metrics
		return self.inCoreQueue
        
