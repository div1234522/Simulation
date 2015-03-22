class System:
    def __init__(self, cores = 5, thread = 50, delay = 1 , quantum = 10):
        self.noOfThread = thread
        self.noOfCores = cores
        self.switchingDelay = delay
        self.quantumSize = quantum
