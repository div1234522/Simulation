class EventList:
	
	#class constructor
	def __init__(self):
		self.h = []
	#for insertion in list	
	def insert(self, ev):
		self.h.append(ev)
		self.h = sorted(self.h, key=lambda ev: ev.timestamp, reverse=True)
	
	#delete and fet the element from list
	def extract(self):
		return self.h.pop()
	
	#returns no of element in list
	def getsize(self):
		return len(self.h)
