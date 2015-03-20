class Cores:
    isSwithing = False
    isBusy = False
    nextQuantumTime = 0
    
    def __init__(self, core = 0,thread = 0):
        self.coreId = core
        self.threadId = thread

    def setIsSwitching(self, switching):
        self.isSwithing = switching

    def getIsSwitching(self):
        return self.isSwithing

    def setIsBusy(self, busy):
        self.isBusy = busy

    def getIsBusy(self):
        return self.isBusy
