import tkinter as tk
from tkinter import messagebox
from Process import Process
from Scheduler import MultiQueueScheduler
import matplotlib.pyplot as plt

class SchedulerGUI:
    def __init__(self, root):
        # Initialize the scheduler and the main window
        self.scheduler = MultiQueueScheduler()
        self.root = root
        self.root.title("Multilevel Queue Scheduler")
        self.root.geometry("900x800")
        self.root.configure(bg="#2E3440")

        # Define the visual style of the GUI
        self.font_main = ("Helvetica", 12)
        self.bg_color = "#2E3440"
        self.text_color = "#D8DEE9"
        self.button_color = "#4C566A"
        self.entry_color = "#3B4252"

        # Create the main container for the input fields and controls
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, pady=10)

        # Build the different parts of the GUI
        self._create_inputs()  # Input fields for process details
        self._create_parameters()  # Customizable parameters like Time Quantum
        self._create_buttons()  # Action buttons (Add, Schedule, Gantt Chart, Reset)
        self._create_metrics_display()  # Display area for metrics

    def _create_inputs(self):
        # Add input fields for process details
        labels = ["Process ID", "Arrival Time", "Burst Time", "Queue (1/2/3)", "Priority (1=High, 2=Med, 3=Low)"]
        self.entries = []

        for i, label in enumerate(labels):
            # Create a label and input box for each field
            tk.Label(self.main_frame, text=label, bg=self.bg_color, fg=self.text_color, font=self.font_main).grid(
                row=i, column=0, pady=5, padx=10, sticky="e")
            entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            self.entries.append(entry)

    def _create_parameters(self):
        # Add customizable parameters for scheduling
        tk.Label(self.main_frame, text="Custom Parameters", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 14)).grid(
            row=5, columnspan=2, pady=10
        )

        # Input for Time Quantum (used in Round Robin)
        self.time_quantum_label = tk.Label(self.main_frame, text="Time Quantum (RR):", bg=self.bg_color, fg=self.text_color, font=self.font_main)
        self.time_quantum_label.grid(row=6, column=0, pady=5, padx=10, sticky="e")

        self.time_quantum_entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
        self.time_quantum_entry.grid(row=6, column=1, pady=5, padx=10, sticky="w")
        self.time_quantum_entry.insert(0, str(self.scheduler.time_quantum))

        # Input for Maximum Process Limit
        self.process_limit_label = tk.Label(self.main_frame, text="Max Processes:", bg=self.bg_color, fg=self.text_color, font=self.font_main)
        self.process_limit_label.grid(row=7, column=0, pady=5, padx=10, sticky="e")

        self.process_limit_entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
        self.process_limit_entry.grid(row=7, column=1, pady=5, padx=10, sticky="w")
        self.process_limit_entry.insert(0, str(self.scheduler.process_limit))

    def _create_buttons(self):
        # Add buttons for performing actions
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        # Button to add a process
        self.add_button = tk.Button(button_frame, text="Add Process", bg=self.button_color, fg=self.text_color,
                                    font=self.font_main, width=15, command=self.add_process)
        self.add_button.grid(row=0, column=0, padx=5)

        # Button to schedule processes
        self.schedule_button = tk.Button(button_frame, text="Schedule", bg=self.button_color, fg=self.text_color,
                                         font=self.font_main, width=15, command=self.schedule)
        self.schedule_button.grid(row=0, column=1, padx=5)

        # Button to visualize the Gantt Chart
        self.visualize_button = tk.Button(button_frame, text="Gantt Chart", bg=self.button_color, fg=self.text_color,
                                          font=self.font_main, width=15, command=self.visualize_gantt_chart)
        self.visualize_button.grid(row=0, column=2, padx=5)

        # Button to reset the scheduler
        self.reset_button = tk.Button(button_frame, text="Reset Scheduler", bg=self.button_color, fg=self.text_color,
                                      font=self.font_main, width=15, command=self.reset_scheduler)
        self.reset_button.grid(row=0, column=3, padx=5)

    def _create_metrics_display(self):
        # Add a display area for metrics (Waiting Time, Turnaround Time)
        tk.Label(self.main_frame, text="Metrics", bg=self.bg_color, fg=self.text_color, font=self.font_main).grid(
            row=9, columnspan=2, pady=10
        )

        self.metrics_text = tk.Text(self.main_frame, height=24, width=90, bg=self.entry_color, fg=self.text_color,
                                    font=("Courier", 12), wrap=tk.WORD)
        self.metrics_text.grid(row=10, column=0, columnspan=2, pady=5, padx=10)

    def add_process(self):
        try:
            # Gather and validate process details from user inputs
            for entry, label in zip(self.entries, ["Process ID", "Arrival Time", "Burst Time", "Queue", "Priority"]):
                if not entry.get().strip():
                    raise ValueError(f"{label} cannot be empty. Please provide a valid value.")
                if not entry.get().strip().isdigit():
                    raise ValueError(f"{label} must be a valid integer.")

            pid, arrival, burst, queue, priority = (int(e.get()) for e in self.entries)

            # Ensure Queue and Priority values are within valid ranges
            if queue not in [1, 2, 3]:
                raise ValueError("Queue must be 1 (High Priority), 2 (Medium Priority), or 3 (Low Priority).")
            if priority not in [1, 2, 3]:
                raise ValueError("Priority must be 1 (High), 2 (Medium), or 3 (Low).")

            # Check if the process ID already exists
            for process in (list(self.scheduler.high_priority_queue) +
                            list(self.scheduler.medium_priority_queue) +
                            list(self.scheduler.low_priority_queue)):
                if process.pid == pid:
                    raise ValueError(f"Process ID {pid} already exists! Please use a unique ID.")

            # Add the process to the scheduler
            process = Process(pid, arrival, burst, queue, priority=priority)
            if self.scheduler.add_process(process):
                messagebox.showinfo("Success", f"Process {pid} added successfully!")
            else:
                messagebox.showerror("Error", "Process limit reached!")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def schedule(self):
        try:
            # Update scheduler parameters based on user inputs
            new_time_quantum = int(self.time_quantum_entry.get()) if self.time_quantum_entry.get().strip() else self.scheduler.time_quantum
            new_process_limit = int(self.process_limit_entry.get()) if self.process_limit_entry.get().strip() else self.scheduler.process_limit

            if new_time_quantum <= 0 or new_process_limit <= 0:
                raise ValueError("Time quantum and process limit must be positive integers.")

            self.scheduler.time_quantum = new_time_quantum
            self.scheduler.process_limit = new_process_limit

            # Check if there are any processes to schedule
            if not self.scheduler.high_priority_queue and not self.scheduler.medium_priority_queue \
                    and not self.scheduler.low_priority_queue:
                messagebox.showerror("Scheduling Error", "No processes added. Please add processes first!")
                return

            # Perform scheduling and display metrics
            self.scheduler.schedule_processes()
            self.metrics_text.delete("1.0", tk.END)
            self.metrics_text.insert(tk.END, "{:<5}{:<15}{:<15}\n".format("PID", "Waiting Time", "Turnaround Time"))
            self.metrics_text.insert(tk.END, "-" * 40 + "\n")

            for metric in self.scheduler.calculate_metrics():
                self.metrics_text.insert(tk.END, "{:<5}{:<15}{:<15}\n".format(
                    metric['PID'], metric['Waiting Time'], metric['Turnaround Time']
                ))

            # Calculate and display average metrics
            metrics = self.scheduler.calculate_metrics()
            avg_waiting_time = sum(m['Waiting Time'] for m in metrics) / len(metrics)
            avg_turnaround_time = sum(m['Turnaround Time'] for m in metrics) / len(metrics)
            self.metrics_text.insert(tk.END, "\nAverage Waiting Time: {:.2f}\n".format(avg_waiting_time))
            self.metrics_text.insert(tk.END, "Average Turnaround Time: {:.2f}\n".format(avg_turnaround_time))

        except ValueError as e:
            messagebox.showerror("Input Error", f"{e}")

    def visualize_gantt_chart(self):
        if not self.scheduler.completed_processes:
            messagebox.showerror("Visualization Error", "No processes to display! Add and schedule processes first.")
            return

        plt.close('all')  # Close any previously opened figures

        # Prepare data for the Gantt chart
        start_times = [p.start_time for p in self.scheduler.completed_processes]
        durations = [p.burst for p in self.scheduler.completed_processes]
        labels = [f"P{p.pid}" for p in self.scheduler.completed_processes]
        priorities = [p.queue for p in self.scheduler.completed_processes]

        colors = {1: "#FF6F61", 2: "#6B5B95", 3: "#88B04B"}

        # Create the Gantt chart with a modern design
        fig, ax = plt.subplots(figsize=(15, 8))  # Adjusted size for clarity
        fig.patch.set_facecolor("#2E3440")  # Dark background for Gantt chart
        ax.set_facecolor("#2E3440")
        ax.tick_params(colors="#D8DEE9", labelsize=12)
        ax.spines['top'].set_color("#D8DEE9")
        ax.spines['bottom'].set_color("#D8DEE9")
        ax.spines['left'].set_color("#D8DEE9")
        ax.spines['right'].set_color("#D8DEE9")

        bars = ax.barh(labels, durations, left=start_times, color=[colors[p] for p in priorities], edgecolor="#D8DEE9")

        # Add gridlines
        ax.xaxis.grid(color="#4C566A", linestyle="--", linewidth=0.7)
        ax.yaxis.grid(color="#4C566A", linestyle="--", linewidth=0.7)
        ax.set_xticks(range(0, int(max(start_times) + max(durations) + 5), 5))  # Time markers every 5 units

        # Set labels and title
        ax.set_xlabel("Time", color="#D8DEE9", fontsize=14, weight="bold")
        ax.set_ylabel("Processes", color="#D8DEE9", fontsize=14, weight="bold")
        ax.set_title("Gantt Chart: Process Execution Timeline", color="#D8DEE9", fontsize=16, weight="bold")

        # Add legend for priorities with modern styling
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[q], ec="#D8DEE9", lw=1.2) for q in colors]
        labels = ["High Priority", "Medium Priority", "Low Priority"]
        legend = ax.legend(handles, labels, loc="upper right", frameon=True, fontsize=12)
        legend.get_frame().set_facecolor("#3B4252")
        legend.get_frame().set_edgecolor("#D8DEE9")

        plt.tight_layout()
        plt.show()

    def reset_scheduler(self):
        """Clear the current state and reset the scheduler."""
        self.scheduler.reset_scheduler()  # Clear the internal scheduler state
        self.metrics_text.delete("1.0", tk.END)  # Clear the metrics display box
        #Deletes the saved input states
        for entry in self.entries:
            entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Scheduler has been reset!")
