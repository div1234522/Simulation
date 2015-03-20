import queue

class CoreQueue:
	queueLength = 10
	
	def __init__(self):
		self.q = queue.Queue(maxsize=CoreQueue.queueLength)
		
	def enqueue(self, req):
		if self.q.full() == False: 
			self.q.put(req)
		
	def dequeue(self):
		if self.q.empty() == False:
			return self.q.get()
	
	def getsize(self):
		return self.q.qsize()
		