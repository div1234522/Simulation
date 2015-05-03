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
good_put = 0
bad_put = 0
def main():
	#prev_size = 0
	# no of clients, thread pool, stream/seed
	inputFile = open('inputFile.txt','r')
	good_put = 0
	
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
			#print('No. of runs: ' + str(simulationRuns))
		if a[0] == 'Stopping criteria for runs(time)':
			depart = int(a[1])
	
	def process_arrival_if_queues_full(): #Function for Handling arrivals if queues are full
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution(ttype,tmean,)
		r[length].setArrivalTimeDistribution(atype,amean,ahigh)
		r[length].clientId = r[ev.requestId].clientId
		timeout[length] = r[length].getTimeOut()
		
		r[length].timestamp = ev.timestamp + r[length].getArrivalTime() + timeout[ev.requestId]
		r[length].setServiceTimeDistribution(stype,smean,shigh)
		serv_time = r[length].getServiceTime()
		r[length].remainingServiceTime = serv_time
		r[length].totalServiceTime = serv_time
		timestamp[length] = r[length].timestamp
		
		e = Event(r[length].timestamp, str(0), r[length].requestId) #Set event for arrival after timeout
		e.setEventType('scheduleArrival')
		ev_list.insert(e)
	
	def process_arrival_if_threads_busy(): #Function for Handling arrivals if all threads are busy
		if sq.getsize() == 0:
			push_from_server_queue()
			#print('here1')
		elif sq.getsize() > 0:
			#print('here2')
			if ev.requestId == sq.getTopElement().requestId: #Check if it is the first element of server queue
				#print('here3')
				push_from_server_queue()
			
	def push_from_server_queue():
		#if tp.getNoOfBusyThreads() != s.noOfThread:
		x = Ind() #Return index of free thread
		print('Ind: ' + str(x))
		if x != -1: #Free thread found
			re = sq.dequeue()
			#print('here4')
			re.timestamp = ev.timestamp
			timestampTrue[re.requestId] = ev.timestamp
			
			re.inCoreQueue = True
			thread[x][1] = 'busy'
			t[x+1].requestId = re.requestId
			t[1].setNoOfBusyThreads(1)
			coreId = (x % s.noOfCores) + 1
			cq[coreId].enqueue(re)
			waitTime[re.requestId] = ev.timestamp - timestamp[re.requestId]
			timestampTrue[re.requestId] = ev.timestamp
			#print("Core id: " + str(coreId) + ' for request: ' + str(req.requestId))
			
			e = Event(re.timestamp, coreId, re.requestId)
			#Core Id: 1-5 - CoreQueue Number
			e.setEventType('arrival')
			ev_list.insert(e)
	
	def process_arrival_if_threads_free(): #Function for Handling arrivals if some threads are free
		ci = ev.coreId
		if cq[int(ci)].getsize() > 0:
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
		serviceTime[ev.requestId] = ev.timestamp - timestampTrue[ev.requestId]
		length = len(r)+1
		r[length] = Request()
		r[length].setTimeOutDistribution(ttype,tmean,thigh)
		timeout[length] = r[length].getTimeOut()
		r[length].setArrivalTimeDistribution(atype,amean,ahigh)
		r[length].clientId = r[ev.requestId].clientId
		thinkTime = c[r[length].clientId].getThinkTimeValue()
		
		r[length].timestamp = ev.timestamp + r[length].getArrivalTime() + thinkTime
		timestamp[length] = r[length].timestamp
		r[length].setServiceTimeDistribution(stype,smean,shigh)
		serv_time = r[length].getServiceTime()
		r[length].remainingServiceTime = serv_time
		r[length].totalServiceTime = serv_time
		thread[r[ev.requestId].threadId - 1][1] = 'free'			
		t[1].setNoOfBusyThreads(-1)
		
		e = Event(r[length].timestamp, str(0), r[length].requestId) #Set event for arrival after thinking
		e.setEventType('scheduleArrival')
		ev_list.insert(e)
		
		if sq.getsize() > 0:
			#print('here5')
			push_from_server_queue() #Push a new element from server queue to core queue empty place
			
	def process_quantumDone(): #Function for Handling quantumDone
		if timeout[ev.requestId] + timestamp[ev.requestId] < ev.timestamp:
			global bad_put
			bad_put += 1
			#print(bad_put)
			#print('Req ' + str(ev.requestId) + ' timedout.')
			rr = cq[int(ev.coreId)].dequeue()
			thread[r[ev.requestId].threadId - 1][1] = 'free'			
			t[1].setNoOfBusyThreads(-1)
			if cq[int(ev.coreId)].getsize() > 0:
				r_next = cq[int(ev.coreId)].getTopElement()
				e = Event(ev.timestamp + s.switchingDelay, ev.coreId, r_next.requestId)
				e.setEventType('service')
				ev_list.insert(e)
			if sq.getsize() > 0:
				push_from_server_queue()
		else:
			if r[ev.requestId].remainingServiceTime == 0:
				e = Event(ev.timestamp, ev.coreId, ev.requestId)
				e.setEventType('departure')
				ev_list.insert(e)
				resTime[ev.requestId] = ev.timestamp - timestamp[ev.requestId]
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
		print('Ind: ' + str(x))
		if x == -1: #No free thread found
			if sq.getsize() >= 100:
				#print('here7')
				coreId = -2 #'discarded'
			else:
				sq.enqueue(req)
				#print('here6')
				coreId = -1 #'serverQueue'
		else:
			req.inCoreQueue = True
			thread[x][1] = 'busy'
			t[x+1].requestId = req.requestId
			t[x+1].setNoOfBusyThreads(1)
			coreId = (x % s.noOfCores) + 1
			cq[coreId].enqueue(req)
			waitTime[req.requestId] = ev.timestamp - timestamp[req.requestId]
			timestampTrue[req.requestId] = ev.timestamp
		#print("Core id: " + str(coreId) + ' for request: ' + str(req.requestId))
		
		e = Event(req.timestamp, coreId, req.requestId)
		#Core Id: 1-5 - CoreQueue Number
		e.setEventType('arrival')
		ev_list.insert(e)
	
	def Ind(): #Return index of free thread
		for i in range(50):				
			if thread[i][1] == 'free':
				return i
		return -1 #No free thread found
	
	s = System(cores,threads,delay,quantum)
	
	sm = Simulation(55,depart,simulationRuns)
	
	rq = Request()
	tp = ThreadPool(50,20,10)
		
	#global metrics
	global_no_of_reqs = 0
	global_total_time_of_sim = 0
	global_bad_put = 0
	global_good_put = 0
	global_no_of_busy_threads = 0
	global_no_of_reqs_in_server_queue = 0
	global_no_of_reqs_in_core_queue = {}
	for i in range(s.noOfCores):
		global_no_of_reqs_in_core_queue[i+1] = 0
	global_no_of_reqs_dropped = 0
	global_waiting_time = 0
	global_service_time = 0
	global_response_time = 0
	global_time_spent_in_switching = 0
	global_cpu_util = 0
	#global metrics
	for runs in range(1,sm.no_of_runs + 1):
		#metrics 
		timestamp = {}
		counter = 0
		req_drop = 0
		reqInServerQueue = 0
		reqInCoreQueue = {}
		departure = {}
		resTime = {}
		waitTime = {}
		timeout = {}
		timestampTrue ={}
		serviceTime= {}
		switchCounter = 0
		good_put = 0
		global bad_put
		bad_put = 0
		
		for i in range(s.noOfCores):
			reqInCoreQueue[i+1] = 0
		last_cpu_busy_time = 0
		cpu_util = 0
		#metrics 
		
		rq.zero()
		tp.zero()
		#print(runs)
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
			timeout[i] = r[i].getTimeOut()
			r[i].setArrivalTimeDistribution(atype,amean,ahigh)
			r[i].timestamp = r[i].getArrivalTime()
			r[i].setServiceTimeDistribution(stype,smean,shigh)
			serv_time = r[i].getServiceTime()
			r[i].remainingServiceTime = serv_time
			r[i].totalServiceTime = serv_time
			r[i].clientId = (i % noOfClients)+1
			timestamp[i] = r[i].timestamp

			#print('New req ' + str(r[i].requestId) + ' timestamp: ' + str(r[i].timestamp) + ' total service: ' + str(r[i].totalServiceTime))
			
			e = Event(r[i].timestamp, str(0), r[i].requestId) #Set event for arrival after timeout
			e.setEventType('scheduleArrival')
			ev_list.insert(e)
		oldTimestamp = 0
		total = 0
		init_time = 0
		while(init_time < sm.stop): #Stopping criteria for simulation
			print(ev_list.getsize())
			# if ev_list.getsize() == 0:
				# print("Simulation ended")
				# break
			# else: #Call appropriate event handler
			ev = ev_list.extract()
			total += ((ev.timestamp-oldTimestamp)*tp.getNoOfBusyThreads())
			oldTimestamp = ev.timestamp
			if cq[1].getsize() == 0 and cq[2].getsize() == 0 and cq[3].getsize() == 0 and cq[4].getsize() == 0 and cq[5].getsize() == 0:
				last_cpu_busy_time = ev.timestamp
			else:
				cpu_util += ev.timestamp - last_cpu_busy_time
				last_cpu_busy_time = ev.timestamp
			
			if ev.eventType == 'arrival':
				counter += 1
				reqInServerQueue += sq.getsize()
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
				
				if ev.coreId == -2: #'discarded': #Request Discarded
					process_arrival_if_queues_full()
					req_drop += 1
				elif ev.coreId == -1: #'serverQueue': #In Server Queue
					process_arrival_if_threads_busy()
				else: #In Core Queue
					process_arrival_if_threads_free()
				
			if ev.eventType == 'quantumDone':
				counter += 1
				reqInServerQueue += sq.getsize()
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
					
				process_quantumDone()
				
			if ev.eventType == 'switchingDone':
				counter += 1
				reqInServerQueue += sq.getsize()
				switchCounter += 1
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
				process_switchingDone()
				
			if ev.eventType == 'departure':
				counter += 1
				reqInServerQueue += sq.getsize()
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
				process_departure()
				good_put += 1
				# if depart_limit == sm.stop:
					# print('departure time of last departure for run ' + str(runs) + ' : ' + str(ev.timestamp))			
				#print('Time of departure ' + str(depart_limit) + ' for run ' + str(runs) + ' : ' + str(ev.timestamp))			
				
			if ev.eventType == 'scheduleArrival':
				counter += 1
				reqInServerQueue += sq.getsize()
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
				process_scheduleArrival()
				
			if ev.eventType == 'service':
				counter += 1
				reqInServerQueue += sq.getsize()
				for i in range(s.noOfCores):
					reqInCoreQueue[i+1] += cq[i+1].getsize()
				process_service()
			
			init_time = ev.timestamp
			# if sq.getsize() in range(2,60): #!= prev_size: 
				# prev_size = sq.getsize()
				# print('Server queue size: ' + str(sq.getsize()))
			#if ev.eventType not in ['arrival', 'scheduleArrival']:
			#print('Size of server queue: ' + str(sq.getsize()))
			print('Timestamp: ' + str(ev.timestamp) + ' Size of core queues: ' + str(cq[1].getsize()) + ' ' + str(cq[2].getsize()) + ' ' + str(cq[3].getsize()) + ' ' + str(cq[4].getsize()) + ' ' + str(cq[5].getsize()) + ' Size of server queue: ' + str(sq.getsize()))
				#print('Processing event: ' + ev.eventType + ' timestamp: ' +str(ev.timestamp) + ' requestId: ' +str(ev.requestId) +' coreId: '+ str(ev.coreId))
			# print('Size of event list: ' + str(ev_list.getsize()))
			# print('no of busy thread: '+str(tp.getNoOfBusyThreads()))
		print(80*'-')
		print('RUN NO: ' + str(runs))
		print('Total number of requests: ' + str(len(waitTime)))
		print('Total time of simulation: ' + str(ev.timestamp/1000) + ' secs')
		print('Good Put: ' + str((1000*good_put)/ev.timestamp) + ' reqs/sec') #For msec to sec
		global bad_put
		bad = bad_put
		print('Bad Put: ' + str((1000*bad)/ev.timestamp) + ' reqs/sec') #For msec to sec
		print('Throughput: ' + str((1000*(good_put + bad))/ev.timestamp) + ' reqs/sec') #For msec to sec
		print('Avg number of busy threads:'+ str(float(total)/ev.timestamp) + ' out of max ' + str(s.noOfThread))
		print('avg no of request in server queue: '+str(float(reqInServerQueue/counter)) + ' out of max ' + str(sq.queueLength))
				
		avg_wait = sum(waitTime)/len(waitTime)
		avg_res = sum(resTime)/len(resTime)
		avg_serv = sum(serviceTime)/len(serviceTime)
		
		for i in range(s.noOfCores):
			print('avg no of request in core queue '+str(i+1)+ ' : '+str(float(reqInCoreQueue[i+1]/counter)) + ' out of max ' + str(cq[i+1].queueLength))
	
		print('Number of reqs dropped: ' + str(req_drop))
		print("waiting time: ", end = '')
		print(str(avg_wait/1000) + ' secs')
		print("service time: ", end = '')
		print(str(avg_serv/1000) + ' secs')
		print("response time: ", end = '')
		print(str((avg_wait+avg_serv)/1000) + ' secs')
		print("Time spent in switching: ", end= '')
		print(str((switchCounter*s.switchingDelay)/1000) + ' secs')
		print('CPU Util: ' + str(cpu_util/ev.timestamp))
		
		
		global_no_of_reqs += len(waitTime)
		global_total_time_of_sim += ev.timestamp
		global bad_put
		bad = bad_put
		global_bad_put += bad/ev.timestamp
		global_good_put += good_put/ev.timestamp
		global_no_of_busy_threads += float(total)/ev.timestamp
		global_no_of_reqs_in_server_queue += float(reqInServerQueue/counter)
		for i in range(s.noOfCores):
			global_no_of_reqs_in_core_queue[i+1] += float(reqInCoreQueue[i+1]/counter)
		global_no_of_reqs_dropped += req_drop
		global_waiting_time += avg_wait
		global_service_time += avg_serv
		global_response_time += avg_wait+avg_serv
		global_time_spent_in_switching += switchCounter*s.switchingDelay
		global_cpu_util += cpu_util/ev.timestamp
		
	print(80*'-')
	print(80*'-')
	print('No of clients: ' + str(noOfClients))
	print('No of threads: ' + str(threads))
	print('Switching delay: ' + str(delay/1000) + ' sec')
	print('Quantum size: ' + str(quantum/1000) + ' sec')
	print('Service Time Mean: ' + str(smean/1000) + ' sec')
	print('Arrival Time Mean: ' + str(amean/1000) + ' sec')
	print('Thinking Time Mean: ' + str(thmean/1000) + ' sec')
	print('Timeout Mean: ' + str(tmean/1000) + ' sec')		
	print(80*'-')
	print(80*'-')
	print('AVERAGE METRICS FOR ALL RUNS:')
	print('Total number of requests: ' + str(global_no_of_reqs/sm.no_of_runs))
	print('Total time of simulation: ' + str(global_total_time_of_sim/(1000*sm.no_of_runs)))
	print('Good put: ' + str((1000*global_good_put)/sm.no_of_runs) + ' reqs/sec')
	print('Bad put: ' + str((1000*global_bad_put)/sm.no_of_runs) + ' reqs/sec')
	print('Throughput: ' + str((1000*(global_good_put + global_bad_put))/sm.no_of_runs))
	print('Avg number of busy threads: '+ str(global_no_of_busy_threads/sm.no_of_runs) + ' out of max ' + str(s.noOfThread))
	print('avg no of request in server queue: '+str(global_no_of_reqs_in_server_queue/sm.no_of_runs) + ' out of max ' + str(sq.queueLength))
	
	for i in range(s.noOfCores):
		print('avg no of request in core queue '+str(i+1)+ ' : '+str(global_no_of_reqs_in_core_queue[i+1]/sm.no_of_runs) + ' out of max ' + str(cq[i+1].queueLength))

	print('Number of reqs dropped: ' + str(global_no_of_reqs_dropped/sm.no_of_runs))
	print("waiting time: ", end = '')
	print(str(global_waiting_time/(1000*sm.no_of_runs)) + ' secs')
	print("service time: ", end = '')
	print(str(global_service_time/(1000*sm.no_of_runs)) + ' secs')
	print("response time: ", end = '')
	print(str(global_response_time/(1000*sm.no_of_runs)) + ' secs')
	print("Time spent in switching: ", end= '')
	print(str(global_time_spent_in_switching/(1000*sm.no_of_runs)) + ' secs')
	print('CPU Util: ' + str(global_cpu_util/sm.no_of_runs))		
	print(80*'-')
	print(80*'-')
		
if __name__ == "__main__": #Place holder for calling main function
	main()
