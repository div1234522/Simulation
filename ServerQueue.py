import queue #For using queue functions

class ServerQueue:
	
	def __init__(self): #Class constructor
		self.queueLength = 100 #Max Queue length
		self.q = queue.Queue(maxsize=self.queueLength)
		
	def enqueue(self, req): #Add to the end of the queue
		if self.q.full() == False: 
			self.q.put(req)
		
	def dequeue(self): #Extract from the front of the queue
		if self.q.empty() == False:
			return self.q.get()
	
	def getsize(self): #Returns current size of queue
		return self.q.qsize()
		
	def getTopElement(self):
		re = self.dequeue()
		self.enqueue(re)
		for i in range(self.getsize() - 1):
			temp = self.dequeue()
			self.enqueue(temp)
		return re
		