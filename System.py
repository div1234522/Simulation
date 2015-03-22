class System:
    def __init__(self, cores = 5, thread = 50, delay = 1 , quantum = 10): #Set criteria for system variables
        self.noOfThread = thread
        self.noOfCores = cores
        self.switchingDelay = delay
        self.quantumSize = quantum
