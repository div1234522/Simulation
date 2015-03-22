from Client import Client
from CoreQueue import CoreQueue
from Event import Event
from EventList import EventList
from Request import Request
from ServerQueue import ServerQueue
from Simulation import Simulation
from System import System
from ThreadPool import ThreadPool
from Cores import Cores
def main():
	def Ind():
		ind = 0
		for i in thread:				
			if i[1] == 'free':
				return ind
			ind += 1
		return -1
	
	sm = Simulation()
	client = []
	c = {}
	for i in range(1,6):
		c[i] = Client()
	print('Clients:', end = ' ')
	for i in range(5):
		print(str(c[i+1].clientId), end=' ')
				
	sys = System(5,50,1,10)
	cq = {}
	for i in range(sys.noOfCores):
		cq[i+1] = CoreQueue()
		#print('Core Queue ' + str(cq.index(cq)) + ' size: ' + str(cq.getsize()))
	sq = ServerQueue()
	#print('Server Queue size: ' + str(sq.getsize()))
		
	ev_list = EventList()
	print('Event List size: ' + str(ev_list.getsize()))

	tp = ThreadPool(50,20,10)
	print("busy thread " + str(tp.getNoOfBusyThreads()))
	print("thread ID " + str(tp.threadId))
	print("coreId " + str(tp.coreId))
	print("req Id " + str(tp.requestId))
	
	"""e = Event(2,51,23)
	print("coreId " + str(e.coreId))
	print("req Id " + str(e.requestId))
	print("timestamp " + str(e.timestamp))
	print("previous type " + e.eventType)
	e.setEventType("arrival")
	print("next type " + e.eventType)"""
	
	"""r = Request(1,1,5,1)
	r.setTimeOutDistribution('exponential',150,1)
	r.setArrivalTimeDistribution('exponential',15,1)
	r.setserviceTimeDistribution('exponential',70,1)
	print('Request1 ID: ' + str(r.requestId))
	r2 = Request(1,1,5,1)
	print('Request1 ID: ' + str(r2.requestId))
	r3 = Request(1,1,5,1)
	print('Request1 ID: ' + str(r3.requestId))"""
	
	
	#run
	s = System(5,50,1,10)
	c = {}
	t = {}
	count = 0
	
	#t = ThreadPool(-1,-1,-1)
	thread = []
	for i in range(1,s.noOfCores+1):
		c[i] = Cores(i,10)
		for j in range(1,(int(s.noOfThread/s.noOfCores))+1):
			count += 1
			t[count] = ThreadPool(count,(count%s.noOfCores)+1,-1)
			a = [count,'free']
			thread.append(a)

	print(c[1].coreId)
	print(c[2].coreId)
	print(c[3].coreId)
	print(c[4].coreId)
	print(c[5].coreId)
	
	
	maxTime = 151
	r= {}
	for i in range(maxTime):
		r[i] = Request(i)
		r[i].setTimeOutDistribution('exponential',150,1)
		r[i].setArrivalTimeDistribution('exponential',15,1)
		r[i].setServiceTimeDistribution('exponential',70,1)
		r[i].remainingServiceTime = r[i].getServiceTime()
		r[i].totalServiceTime = r[i].getServiceTime()
		r[i].clientId = (i % 5)+1
		x = Ind()
		if x == -1:
		
			if sq.getsize() >= 100:
				print("request dropped:" + str(r[i].requestId))
				r[1].requestId = -1
			else:
				sq.enqueue(r[i])
		else:
			r[i].inCoreQueue = True
			thread[x][1] = 'busy'
			t[x+1].requestId = r[i].requestId
			t[x+1].setNoOfBusyThreads(1)
		
		
if __name__ == "__main__":
	main()
