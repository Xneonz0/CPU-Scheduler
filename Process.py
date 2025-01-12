class Process:
    def __init__(self, pid, arrival, burst, queue, priority=3):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.queue = queue
        self.priority = priority  
        self.remaining_time = burst
        self.start_time = None
        self.finish_time = None

    def __str__(self):
        return (f"PID: {self.pid}, Arrival: {self.arrival}, Burst: {self.burst}, "
                f"Queue: {self.queue}, Priority: {self.priority}")
