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
	#Extract from the front of the queue	
	def dequeue(self):
		if self.q.empty() == False:
			return self.q.get()
	#it will give no of element in queue
	def getsize(self):
		return self.q.qsize()
		
	def getTopElement(self):
		re = self.dequeue()
		self.enqueue(re)
		for i in range(self.getsize() - 1):
			temp = self.dequeue()
			self.enqueue(temp)
		return re
		