class Cores:
	#class variables
    isSwitching = False
    isBusy = False
    nextQuantumTime = 0
    
	#class constructor
    def __init__(self, core = 0,thread = 0):
        self.coreId = core
        self.threadId = thread
	
	#set the state of core queue to switching
    def setIsSwitching(self, switching):
        self.isSwitching = switching
	
	#returns the status of core queue
    def getIsSwitching(self):
        return self.isSwitching
	
	#set the state of core queue to busy
    def setIsBusy(self, busy):
        self.isBusy = busy
	
	#returns the status of core queue
    def getIsBusy(self):
        return self.isBusy
