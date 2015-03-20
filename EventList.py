import heapq

class EventList:
	
	def __init__(self):
		self.h = []
		
	def insert(self, ev):
		heappush(self.h, ev) #Auto heapify
		
	def extract(self):
		return heappop(self.h)
	
	def getsize(self):
		return len(self.h)
		