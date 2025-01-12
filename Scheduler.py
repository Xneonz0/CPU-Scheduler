from collections import deque
import matplotlib.pyplot as plt

class MultiQueueScheduler:
    def __init__(self, process_limit=20, time_quantum=2):
        """Initialize the scheduler with process limit and time quantum."""
        self.high_priority_queue = deque()
        self.medium_priority_queue = deque()
        self.low_priority_queue = deque()
        self.completed_processes = []
        self.time_quantum = time_quantum
        self.process_limit = process_limit
        self.process_count = 0

    def reset_scheduler(self):
        """Reset all scheduler data."""
        self.high_priority_queue.clear()
        self.medium_priority_queue.clear()
        self.low_priority_queue.clear()
        self.completed_processes.clear()
        self.process_count = 0

    def add_process(self, process):
        """Add a process to the appropriate queue based on its priority."""
        if self.process_count >= self.process_limit:
            return False
        if process.queue == 1:
            self.high_priority_queue.append(process)
        elif process.queue == 2:
            process.remaining_time = process.burst
            self.medium_priority_queue.append(process)
        elif process.queue == 3:
            self.low_priority_queue.append(process)
        self.process_count += 1
        return True

    def schedule_processes(self):
        """Schedule processes in all queues using the appropriate algorithm."""
        current_time = 0

        # High Priority Queue (Preemptive Priority Scheduling)
        while self.high_priority_queue:
            self.high_priority_queue = deque(sorted(self.high_priority_queue, key=lambda p: (p.priority, p.arrival)))
            process = self.high_priority_queue.popleft()
            if current_time < process.arrival:
                current_time = process.arrival
            if process.remaining_time > 0:
                execution_time = min(process.remaining_time, self.time_quantum)
                process.start_time = process.start_time if process.start_time else current_time
                process.remaining_time -= execution_time
                current_time += execution_time
                if process.remaining_time > 0:
                    self.high_priority_queue.append(process)
                else:
                    process.finish_time = current_time
                    process.waiting_time = process.finish_time - process.arrival - process.burst
                    process.turnaround_time = process.finish_time - process.arrival
                    self.completed_processes.append(process)

        # Medium Priority Queue (Round Robin)
        while self.medium_priority_queue:
            temp_queue = deque()
            while self.medium_priority_queue:
                process = self.medium_priority_queue.popleft()
                if current_time < process.arrival:
                    current_time = process.arrival
                time_slice = min(self.time_quantum, process.remaining_time)
                process.start_time = process.start_time if process.start_time else current_time
                process.remaining_time -= time_slice
                current_time += time_slice
                if process.remaining_time > 0:
                    temp_queue.append(process)
                else:
                    process.finish_time = current_time
                    process.waiting_time = process.finish_time - process.arrival - process.burst
                    process.turnaround_time = process.finish_time - process.arrival
                    self.completed_processes.append(process)
            self.medium_priority_queue = temp_queue

        # Low Priority Queue (Shortest Job First - SJF)
        while self.low_priority_queue:
            self.low_priority_queue = deque(sorted(self.low_priority_queue, key=lambda p: (p.burst, p.arrival)))
            process = self.low_priority_queue.popleft()
            if current_time < process.arrival:
                current_time = process.arrival
            process.start_time = current_time
            current_time += process.burst
            process.finish_time = current_time
            process.waiting_time = process.finish_time - process.arrival - process.burst
            process.turnaround_time = process.finish_time - process.arrival
            self.completed_processes.append(process)

    def calculate_metrics(self):
        """Calculate waiting time and turnaround time for all completed processes."""
        return [
            {"PID": p.pid, "Waiting Time": p.waiting_time, "Turnaround Time": p.turnaround_time}
            for p in self.completed_processes
        ]

    def visualize_gantt_chart(self):
        """Generate a Gantt chart showing process execution timelines."""
        if not self.completed_processes:
            print("No processes to display! Add and schedule processes first.")
            return

        start_times = [p.start_time for p in self.completed_processes]
        durations = [p.burst for p in self.completed_processes]
        labels = [f"P{p.pid}" for p in self.completed_processes]
        priorities = [p.queue for p in self.completed_processes]

        colors = {1: "#FF6F61", 2: "#6B5B95", 3: "#88B04B"}
        plt.barh(labels, durations, left=start_times, color=[colors[p] for p in priorities])
        plt.xlabel("Time")
        plt.ylabel("Processes")
        plt.title("Gantt Chart: Process Execution Timeline")
        plt.legend(handles=[
            plt.Rectangle((0, 0), 1, 1, color=colors[1], label="High Priority"),
            plt.Rectangle((0, 0), 1, 1, color=colors[2], label="Medium Priority"),
            plt.Rectangle((0, 0), 1, 1, color=colors[3], label="Low Priority")
        ])
        plt.show()
