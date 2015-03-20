class Event:
    eventType = ""

    def __init__(self , timestamp , coreId, requestId):
        self.coreId = coreId
        self.requestId = requestId
        self.timestamp  = timestamp
    
    def setEventType(self, event):
        self.eventType = event

    def getEventType(self):
        return self.eventType
