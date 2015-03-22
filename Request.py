class Request:
    inCoreQueue = False
    global request = 0
    def __init__(self, client,time,tservice,rservice,thread)
        self.requestId = Request.request+1
        self.clientId = client
        self.timestamp = time
        self.totalServiceTime = tservice
        self.remainingServiceTime = rservice
        self.threadId = thread
        Request.request +=1
    
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

    def setInCoreQueue(self, queue):
        self.inCoreQueue = queue

    def getInCoreQueue(self):
        return self.inCoreQueue
        
