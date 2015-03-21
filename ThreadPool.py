class ThreadPool:

    def __init__(self, thread , core ,request):
        self.threadId = thread
        self.coreId = core
        self.requestId = request
    
    def setNoOfBusyThreads(self, no):
        self.noOfBusyThreads = no

	def getNoOfBusyThreads(self):
		return self.noOfBusyThreads 