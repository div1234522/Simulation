class ThreadPool:
	global noOfBusyThreads #Keeps track of number of busy threads
	noOfBusyThreads = 0
	
	def __init__(self, thread , core ,request = 'NULL'): #Class constructor
		self.threadId = thread
		self.coreId = core
		self.requestId = request
	
	def setNoOfBusyThreads(self, no): #Assign value of current number of busy threads
		global noOfBusyThreads
		noOfBusyThreads += no
		
	def zero(self):
		global noOfBusyThreads
		noOfBusyThreads = 0

	def getNoOfBusyThreads(self): #Get value of number of busy threads
		return noOfBusyThreads