class EventList:
	
	def __init__(self):
		self.h = []
		
	def insert(self, ev):
		self.h.append(ev)
		self.h = sorted(self.h, key=lambda ev: ev.timestamp, reverse=True)
		
	def extract(self):
		return self.h.pop()
	
	def getsize(self):
		return len(self.h)
