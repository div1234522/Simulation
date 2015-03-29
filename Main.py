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
	noOfClients = 60
	
	def process_arrival_if_queues_full(): #Function for Handling arrivals if queues are full
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution('exponential',150,1)
		r[length].setArrivalTimeDistribution('exponential',15,1)
		r[length].clientId = r[ev.requestId].clientId
		timeout = r[ev.requestId].getTimeout()
		
		r[length].timestamp = r[length-1].timestamp + r[length].getArrivalTime() + timeout
		r[length].setServiceTimeDistribution('exponential',70,1)
		r[length].remainingServiceTime = r[length].getServiceTime()
		r[length].totalServiceTime = r[length].getServiceTime()
		
		pushArrival(r[length]) #Schedule an arrival
	
	def process_arrival_if_threads_busy(): #Function for Handling arrivals if all threads are busy
		if tp.getNoOfBusyThreads() != s.noOfThread:
			re = sq.dequeue()
			re.timestamp = ev.timestamp
			pushArrival(re)
	
	def process_arrival_if_threads_free(): #Function for Handling arrivals if some threads are free
		if r[ev.requestId].remainingServiceTime < s.quantumSize:
			ts = ev.timestamp + r[ev.requestId].remainingServiceTime
		else:
			ts = ev.timestamp + s.quantumSize
		
		r[ev.requestId].remainingServiceTime -= ts
		e = Event(ts, ev.coreId, ev.requestId)
		e.setEventType('quantumDone')
		ev_list.insert(e)
						
	def process_departure(): #Function for Handling departures
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution('exponential',150,1)
		r[length].setArrivalTimeDistribution('exponential',15,1)
		r[length].clientId = r[ev.requestId].clientId
		thinkTime = c[r[length].clientId].getThinkTimeValue()
		
		r[length].timestamp = r[length-1].timestamp + r[length].getArrivalTime() + thinkTime
		r[length].setServiceTimeDistribution('exponential',70,1)
		r[length].remainingServiceTime = r[length].getServiceTime()
		r[length].totalServiceTime = r[length].getServiceTime()
		thread[r[ev.requestId].threadId][1] = 'free'			
		t[1].setNoOfBusyThreads(-1)
		
		e = Event(r[length].timestamp, 0, r[length].requestId) #Set event for arrival after thinking
		e.setEventType('scheduleArrival')
		ev_list.insert(e)
			
	def process_quantumDone(): #Function for Handling quantumDone
		if r[ev.requestId].remainingServiceTime == 0:
			e = Event(ev.timestamp, 0, ev.requestId)
			e.setEventType('departure')
			ev_list.insert(e)
			
		e = Event(ev.timestamp + s.switchingDelay, ev.coreId, ev.requestId)
		e.setEventType('switchingDone')
		ev_list.insert(e)
			
	def process_switchingDone(): #Function for Handling switchingDone
		rr = cq[ev.coreId].dequeue()
		#Todo implement processing of enqueued request
		cq[ev.coreId].enqueue(rr)
			
	def process_scheduleArrival(): #Function for Handling arrival of thinking requests
			pushArrival(r[ev.requestId])
		
	def pushArrival(req): #Function to push a new arrival
		x = Ind() #Return index of free thread
		if x == -1: #No free thread found
			if sq.getsize() >= 100:
				coreId = 'discarded'
			else:
				sq.enqueue(req)
				coreId = 'serverQueue'
		else:
			req.inCoreQueue = True
			thread[x][1] = 'busy'
			t[x+1].requestId = req.requestId
			t[x+1].setNoOfBusyThreads(1)
			coreId = (x % s.noOfCores) + 1
		#print("Core id: " + str(coreId) + ' for request: ' + str(req.requestId))
		
		e = Event(req.timestamp, coreId, req.requestId)
		#Core Id: 1-5 - CoreQueue Number
		e.setEventType('arrival')
		ev_list.insert(e)
	
	def Ind(): #Return index of free thread
		ind = 0
		for i in thread:				
			if i[1] == 'free':
				return ind
			ind += 1
		return -1 #No free thread found
	
	sm = Simulation()
	client = []
	c = {}
	for i in range(1,noOfClients+1):
		c[i] = Client()
		c[i].setThinkTimeDistribution()
				
	sys = System(5,50,1,10)
	cq = {}
	for i in range(sys.noOfCores):
		cq[i+1] = CoreQueue()
	sq = ServerQueue()
		
	ev_list = EventList()

	tp = ThreadPool(50,20,10)
	
	s = System(5,50,1,10)
	co = {}
	t = {}
	count = 0
	
	thread = [] #Create free threads
	for i in range(1,s.noOfCores+1):
		co[i] = Cores(i,10)
		for j in range(1,(int(s.noOfThread/s.noOfCores))+1):
			count += 1
			t[count] = ThreadPool(count,(count%s.noOfCores)+1,-1)
			a = [count,'free']
			thread.append(a)
	
	r = {}
	current_timestamp = 0
	event_processed = 0
	for i in range(1, noOfClients+1): #Generate requests by clients
		r[i] = Request()
		r[i].setTimeOutDistribution('exponential',150,1)
		r[i].setArrivalTimeDistribution('exponential',15,1)
		r[i].timestamp = r[i].getArrivalTime()
		r[i].setServiceTimeDistribution('exponential',70,1)
		r[i].remainingServiceTime = r[i].getServiceTime()
		r[i].totalServiceTime = r[i].getServiceTime()
		r[i].clientId = (i % noOfClients)+1

		pushArrival(r[i]) #Schedule an arrival event
		
	while(event_processed < 1000): #Stopping criteria for simulation
		if ev_list.getsize() == 0:
			print("Simulation ended")
			break
		else: #Call appropriate event handler
			ev = ev_list.extract()
			if ev.eventType == 'arrival':
				if ev.coreId == 'discarded': #Request Discarded
					process_arrival_if_queues_full()
				elif ev.coreId == 'serverQueue': #In Server Queue
					process_arrival_if_threads_busy()
				else: #In Core Queue
					process_arrival_if_threads_free()
				event_processed += 1
			if ev.eventType == 'quantumDone':
				process_quantumDone()
				event_processed += 1
			if ev.eventType == 'switchingDone':
				process_switchingDone()
				event_processed += 1
			if ev.eventType == 'departure':
				process_departure()
				event_processed += 1
			if ev.eventType == 'scheduleArrival':
				process_scheduleArrival()
				event_processed += 1
			
			print('Events Processed: ' + str(event_processed))
			print('Core Queue sizes: ' + str(cq[1].getsize()) + ' ' + str(cq[2].getsize()) + ' ' + str(cq[3].getsize()) + ' ' + str(cq[4].getsize()) + ' ' + str(cq[5].getsize()) + ' ')
			if ev.coreId in range(6):
				print('Timestamp: ' + str(ev.timestamp) + ' type: ' + ev.eventType + ' in core ' + str(ev.coreId))
			else:
				print('Timestamp: ' + str(ev.timestamp) + ' type: ' + ev.eventType + ' in ' + str(ev.coreId))
				
if __name__ == "__main__": #Place holder for calling main function
	main()
