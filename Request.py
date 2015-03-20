class Request:
    clientId = 0
    requestId = 0
    timestamp = 0
    totalServiceTime = 0
    remainingServiceTime = 0
    threadId = 0
    def __init__ (self):
        self.inCoreQueue = "false"

    def setTimeOutDistribution(self, dis_type = "exponential" , mean = 50, variance = 1):
        self.dis_type = dis_type
        self.mean = mean
        self.variance = variance

    def getTimeOut(self):
        val = 0#some cal
        return val

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
