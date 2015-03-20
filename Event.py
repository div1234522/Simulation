class Event:
    eventType = ""

    def __init__(self , time , core, request):
        self.coreId = core
        self.requestId = request
        self.timestamp  = time
    
    def setEventType(self, event):
        self.eventType = event

    def getEventType(self):
        return self.eventType
