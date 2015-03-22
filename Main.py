from Client import Client
from CoreQueue import CoreQueue
from Event import Event
from EventList import EventList
from Request import Request
from ServerQueue import ServerQueue
from Simulation import Simulation
from System import System
from ThreadPool import ThreadPool

def main():
	client = []
	while True:
		c = Client()
		if c.clientId <= Client.maxNoOfClients:
			client.append(c)
		else:
			break
	print('Clients:', end = ' ')
	for i in range(5):
		print(str(client[i].clientId), end=' ')
		
	#Prompt for input of system variables from user here
	sys = System();
		
	print('')
	cq_list = []
	for i in range(sys.noOfCores):
		cq = CoreQueue()
		cq_list.append(cq)
		print('Core Queue ' + str(cq_list.index(cq)) + ' size: ' + str(cq.getsize()))
	sq = ServerQueue()
	print('Server Queue size: ' + str(sq.getsize()))
		
	ev_list = EventList()
	print('Event List size: ' + str(ev_list.getsize()))

	#daulat
	print("----------")
	print("----------")
	print("----------")
	tp = ThreadPool(50,20,10)
	print("busy thread " + str(tp.getNoOfBusyThreads()))
	print("thread ID " + str(tp.threadId))
	print("coreID " + str(tp.coreId))
	print("req Id " + str(tp.requestId))
	print("----------")
	print("----------")
	print("----------")
	e = Event(2,51,23)
	print("coreID " + str(e.coreId))
	print("req Id " + str(e.requestId))
	print("timestamp " + str(e.timestamp))
	print("previous type " + e.eventType)
	e.setEventType("arrival")
	print("next type " + e.eventType)
	
		
if __name__ == "__main__":
	main()
