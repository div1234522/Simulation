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
	
	# no of clients, thread pool, stream/seed
	inputFile = open('inputFile.txt','r')
	for row in inputFile:
		a = row.split('=')
		if a[0] == 'No. of clients':
			noOfClients = int(a[1])
		if a[0] == 'No. of cores':
			cores = int(a[1])
		if a[0] == 'No. of threads':
			threads = int(a[1])
		if a[0] == 'Switching delay':
			delay = int(a[1])
		if a[0] == 'Quantum size':
			quantum = int(a[1])
		if a[0] == 'Service Time Distribution':
			aa = a[1].split(',')
			stype = aa[0]
			shigh = 1
			if stype == 'exponential' or 'constant':
				smean = int(aa[1])
			else:
				shigh = int(aa[2])
			
		if a[0] == 'Arrival Time Distribution':
			aa = a[1].split(',')
			atype = aa[0]
			ahigh = 1
			if atype == 'exponential' or 'constant':
				amean = int(aa[1])
			else:
				ahigh = int(aa[2])
		if a[0] == 'Thinking Time Distribution':
			aa = a[1].split(',')
			thtype = aa[0]
			thhigh = 1
			if thtype == 'exponential' or 'constant':
				thmean = int(aa[1])
			else:
				thhigh = int(aa[2])
		if a[0] == 'Timeout Distribution':
			aa = a[1].split(',')
			ttype = aa[0]
			thigh = 1
			if ttype == 'exponential' or 'constant':
				tmean = int(aa[1])
			else:
				thigh = int(aa[2])
		if a[0] == 'No. of simulation runs':
			simulationRuns = int(a[1])
			print('No. of runs: ' + str(simulationRuns))
		if a[0] == 'Stopping criteria for runs(departure)':
			depart = int(a[1])
			#print(depart)
		#if a[0] == 'Stream/Seed values for every run'
	
	def process_arrival_if_queues_full(): #Function for Handling arrivals if queues are full
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution(ttype,tmean,)
		r[length].setArrivalTimeDistribution(atype,amean,ahigh)
		r[length].clientId = r[ev.requestId].clientId
		timeout = r[ev.requestId].getTimeout()
		
		r[length].timestamp = r[length-1].timestamp + r[length].getArrivalTime() + timeout
		r[length].setServiceTimeDistribution(stype,smean,shigh)
		serv_time = r[length].getServiceTime()
		r[length].remainingServiceTime = serv_time
		r[length].totalServiceTime = serv_time
		
		e = Event(r[length].timestamp, str(0), r[length].requestId) #Set event for arrival after timeout
		e.setEventType('scheduleArrival')
		ev_list.insert(e)
	
	def process_arrival_if_threads_busy(): #Function for Handling arrivals if all threads are busy
		if ev.requestId == sq.getTopElement().requestId: #Check if it is the first element of server queue
			push_from_server_queue()
			
	def push_from_server_queue():
		if tp.getNoOfBusyThreads() != s.noOfThread:
			re = sq.dequeue()
			re.timestamp = ev.timestamp
			pushArrival(re)
	
	def process_arrival_if_threads_free(): #Function for Handling arrivals if some threads are free
		ci = ev.coreId
		if ev.requestId == cq[int(ci)].getTopElement().requestId: #Check if it is the first element of this core queue
			#print('Processing scheduled for requestId: ' + str(ev.requestId))
			e = Event(ev.timestamp, ci, ev.requestId)
			e.setEventType('service')
			ev_list.insert(e)
		
	def process_service(): #CPU Processing
		#print('Processing req: ' + str(ev.requestId) +  ' Time: ' + str(ev.timestamp) + ' remaining Service: ' + str(r[ev.requestId].remainingServiceTime) + ' (before)')
		if r[ev.requestId].remainingServiceTime < s.quantumSize:
			ts = ev.timestamp + r[ev.requestId].remainingServiceTime
			r[ev.requestId].remainingServiceTime = 0
		else:
			ts = ev.timestamp + s.quantumSize
			r[ev.requestId].remainingServiceTime -= s.quantumSize
		
		e = Event(ts, ev.coreId, ev.requestId)
		e.setEventType('quantumDone')
		ev_list.insert(e)
		#print('Processed req: ' + str(ev.requestId) +  ' Time: ' + str(ts) + ' remaining Service: ' + str(r[ev.requestId].remainingServiceTime) + ' (after)')
						
	def process_departure(): #Function for Handling departures
		r_old = cq[int(ev.coreId)].dequeue()
		if cq[int(ev.coreId)].getsize() != 0:
			r_next = cq[int(ev.coreId)].getTopElement()
			e = Event(ev.timestamp + s.switchingDelay, ev.coreId, r_next.requestId)
			e.setEventType('service')
			ev_list.insert(e)
		
		#print('Depart for Req: ' + str(r_old.requestId) + ' Time: ' + str(ev.timestamp) + ' remaining Service: ' + str(r_old.remainingServiceTime))
		
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution(ttype,tmean,thigh)
		r[length].setArrivalTimeDistribution(atype,amean,ahigh)
		r[length].clientId = r[ev.requestId].clientId
		thinkTime = c[r[length].clientId].getThinkTimeValue()
		
		r[length].timestamp = r[length-1].timestamp + r[length].getArrivalTime() + thinkTime
		r[length].setServiceTimeDistribution(stype,smean,shigh)
		serv_time = r[length].getServiceTime()
		r[length].remainingServiceTime = serv_time
		r[length].totalServiceTime = serv_time
		thread[r[ev.requestId].threadId][1] = 'free'			
		t[1].setNoOfBusyThreads(-1)
		
		e = Event(r[length].timestamp, str(0), r[length].requestId) #Set event for arrival after thinking
		e.setEventType('scheduleArrival')
		ev_list.insert(e)
		
		if sq.getsize() > 0:
			push_from_server_queue() #Push a new element from server queue to core queue empty place
			
	def process_quantumDone(): #Function for Handling quantumDone
		if r[ev.requestId].remainingServiceTime == 0:
			e = Event(ev.timestamp, ev.coreId, ev.requestId)
			e.setEventType('departure')
			ev_list.insert(e)
		else:
			e = Event(ev.timestamp + s.switchingDelay, ev.coreId, ev.requestId)
			e.setEventType('switchingDone')
			ev_list.insert(e)
			
	def process_switchingDone(): #Function for Handling switchingDone
		rr = cq[int(ev.coreId)].dequeue()
		cq[int(ev.coreId)].enqueue(rr)
		r_next = cq[int(ev.coreId)].getTopElement()
		e = Event(ev.timestamp + s.switchingDelay, ev.coreId, r_next.requestId)
		e.setEventType('service')
		ev_list.insert(e)
			
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
			coreId = str((x % s.noOfCores) + 1)
			cq[int(coreId)].enqueue(req)
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
	
	s = System(cores,threads,delay,quantum)
	
	sm = Simulation(55,depart,simulationRuns)
	
	rq = Request()
	tp = ThreadPool(50,20,10)
		
	for runs in range(1,sm.no_of_runs + 1):
		rq.zero()
		tp.zero()
		#print(runs
		client = []
		c = {}
		for i in range(1,noOfClients+1):
			c[i] = Client()
			c[i].setThinkTimeDistribution(thtype,thmean,thhigh)
					
		cq = {}
		for i in range(s.noOfCores):
			cq[i+1] = CoreQueue()
		sq = ServerQueue()
			
		ev_list = EventList()
		
		co = {}
		t = {}
		count = 0
		
		thread = [] #Create free threads
		for i in range(1,s.noOfCores+1):
			co[i] = Cores(str(i),10)
			for j in range(1,(int(s.noOfThread/s.noOfCores))+1):
				count += 1
				t[count] = ThreadPool(count,str((count%s.noOfCores)+1),-1)
				a = [count,'free']
				thread.append(a)
		
		r = {}
		
		for i in range(1, noOfClients+1): #Generate requests by clients
			r[i] = Request()
			r[i].setTimeOutDistribution(ttype,tmean,thigh)
			r[i].setArrivalTimeDistribution(atype,amean,ahigh)
			r[i].timestamp = r[i].getArrivalTime()
			r[i].setServiceTimeDistribution(stype,smean,shigh)
			serv_time = r[i].getServiceTime()
			r[i].remainingServiceTime = serv_time
			r[i].totalServiceTime = serv_time
			r[i].clientId = (i % noOfClients)+1

			#print('New req ' + str(r[i].requestId) + ' timestamp: ' + str(r[i].timestamp) + ' total service: ' + str(r[i].totalServiceTime))
			
			e = Event(r[i].timestamp, str(0), r[i].requestId) #Set event for arrival after timeout
			e.setEventType('scheduleArrival')
			ev_list.insert(e)
		
		depart_limit = 0
		while(depart_limit < sm.stop): #Stopping criteria for simulation
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
					
				if ev.eventType == 'quantumDone':
					process_quantumDone()
					
				if ev.eventType == 'switchingDone':
					process_switchingDone()
					
				if ev.eventType == 'departure':
					process_departure()
					depart_limit += 1
					# if depart_limit == sm.stop:
						# print('departure time of last departure for run ' + str(runs) + ' : ' + str(ev.timestamp))			
					#print('Time of departure ' + str(depart_limit) + ' for run ' + str(runs) + ' : ' + str(ev.timestamp))			
					
				if ev.eventType == 'scheduleArrival':
					process_scheduleArrival()
					
				if ev.eventType == 'service':
					process_service()
				
				print('Processing event: ' + ev.eventType + ' timestamp: ' +str(ev.timestamp) + ' requestId: ' +str(ev.requestId) +' coreId: '+ str(ev.coreId))
				#print('no of busy thread: '+str(tp.getNoOfBusyThreads()))
		print('Time of departure ' + str(depart_limit) + ' for run ' + str(runs) + ' : ' + str(ev.timestamp))
		
if __name__ == "__main__": #Place holder for calling main function
	main()
