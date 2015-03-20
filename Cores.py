class Cores:
    isSwithing = False
    isBusy = False
    nextQuantumTime = 0
    
    def __init__(self, coreId = 0,threadId = 0):
        self.coreId = coreId
        self.threadId = threadId

    def setIsSwitching(self, switching):
        self.isSwithing = switching

    def getIsSwitching(self):
        return self.isSwithing

    def setIsBusy(self, busy):
        self.isBusy = busy

    def getIsBusy(self):
        return self.isBusy
