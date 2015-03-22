import numpy
import math

class Request:
	global request
	request = 0
	inCoreQueue = False
	
	def __init__(self, client, time, tservice, thread):
		self.requestId = request+1
		self.clientId = client
		self.timestamp = time
		self.totalServiceTime = tservice
		self.remainingServiceTime = tservice
		self.threadId = thread
		global request
		request +=1
		
	def setTimeOutDistribution(self, dis = "exponential" , mean_value = 50, variance_value = 1):
		self.dis_type = dis
		self.mean = mean_value
		self.variance = variance_value
		
	def getTimeOut(self):
		if self.dis_type == 'exponential':
			return math.ceil(numpy.random.exponential(self.mean))
			
	def setArrivalTimeDistribution(self, dis_type = "exponential" , mean = 50, variance = 1):
		self.dis_type = dis_type
		self.mean = mean
		self.variance = variance
	
	def getArrivalTime(self):
		val = 0 #some cal
		return val
		
	def setserviceTimeDistribution(self, dis_type = "exponential" , mean = 50, variance = 1):
		self.dis_type = dis_type
		self.mean = mean
		self.variance = variance
		
	def getServiceTime(self):
		val = 0 #some cal
		return val
		
	def setInCoreQueue(self, queue):
		self.inCoreQueue = queue
		
	def getInCoreQueue(self):
		return self.inCoreQueue
        
