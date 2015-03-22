import queue

class CoreQueue:
	#size of core queue
	queueLength = 10
	
	#class constructor
	def __init__(self):
		self.q = queue.Queue(maxsize=CoreQueue.queueLength)
	#queue operation for insertion	
	def enqueue(self, req):
		if self.q.full() == False: 
			self.q.put(req)
	#queue operation for deletion	
	def dequeue(self):
		if self.q.empty() == False:
			return self.q.get()
	#it will give no of element in queue
	def getsize(self):
		return self.q.qsize()
		