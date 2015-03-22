class ThreadPool:
	global noOfBusyThreads
	noOfBusyThreads = 0
	
	def __init__(self, thread , core ,request = -1):
		self.threadId = thread
		self.coreId = core
		self.requestId = request
	
	def setNoOfBusyThreads(self, no):
		global noOfBusyThreads
		noOfBusyThreads += no

	def getNoOfBusyThreads(self):
		return noOfBusyThreads