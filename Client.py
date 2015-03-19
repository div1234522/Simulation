class Client:
	maxNoOfClients = 5
	currentNoOfClients = 0
	
	def __init__(self):
		Client.currentNoOfClients += 1
		self.clientId = Client.currentNoOfClients
		self.setIsThinking(False)
		
	def setThinkTimeDistribution(self, dis_type="exponential", mean=5, variance=1):
		self.type = dis_type
		self.mean = mean
		self.variance = variance
		
	def getThinkTimeValue(self):
		#ToDo: Implement this method
		return 5
		
	def setIsThinking(self, value):
		self.isThinking = value
		
	def getIsThinking(self):
		return self.isThinking
		