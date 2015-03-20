import queue

class ServerQueue:
	
	def __init__(self):
		self.queueLength = 100
		self.q = queue.Queue(maxsize=self.queueLength)
		
	def enqueue(self, req):
		if self.q.full() == False: 
			self.q.put(req)
		
	def dequeue(self, req):
		if self.q.empty() == False:
			return self.q.get()
	
	def getsize(self):
		return self.q.qsize()
		