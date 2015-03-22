class Simulation:
	
	def __init__(self, seed_value = 55, stop_value = 500, nor=10): #Set criteria for simulation start
		self.seed = seed_value
		self.stream = 'default'
		self.stop = stop_value
		self.no_of_runs = nor