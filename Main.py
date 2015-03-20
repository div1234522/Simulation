from Client import Client

def main():
	client = []
	while True:
		c = Client()
		if c.clientId <= Client.maxNoOfClients:
			client.append(c)
		else:
			break
	for i in range(5):
		print(client[i].clientId)
		
if __name__ == "__main__":
	main()