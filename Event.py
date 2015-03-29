class Event:
    eventType = 'NULL'
	
	#class constructor
    def __init__(self , time , core, request):
        self.coreId = core
        self.requestId = request
        self.timestamp  = time
    
	#set event type
    def setEventType(self, event):
        self.eventType = event
	
	#get event type
    def getEventType(self):
        return self.eventType
