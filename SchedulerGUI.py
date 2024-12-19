import tkinter as tk
from tkinter import messagebox
from Process import Process
from Scheduler import MultiQueueScheduler
import matplotlib.pyplot as plt

class SchedulerGUI:
    def __init__(self, root):
        self.scheduler = MultiQueueScheduler()
        self.root = root
        self.root.title("Multilevel Queue Scheduler")
        self.root.geometry("900x800")
        self.root.configure(bg="#2E3440")

        self.font_main = ("Helvetica", 12)
        self.bg_color = "#2E3440"
        self.text_color = "#D8DEE9"
        self.button_color = "#4C566A"
        self.entry_color = "#3B4252"

        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, pady=10)

        self._create_inputs()
        self._create_parameters()
        self._create_buttons()
        self._create_metrics_display()

    def _create_inputs(self):
        labels = ["Process ID", "Arrival Time", "Burst Time", "Queue (1/2/3)"]
        self.entries = []

        for i, label in enumerate(labels):
            tk.Label(self.main_frame, text=label, bg=self.bg_color, fg=self.text_color, font=self.font_main).grid(
                row=i, column=0, pady=5, padx=10, sticky="e")
            entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            self.entries.append(entry)

    def _create_parameters(self):
        tk.Label(self.main_frame, text="Custom Parameters", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 14)).grid(
            row=4, columnspan=2, pady=10
        )

        self.time_quantum_label = tk.Label(self.main_frame, text="Time Quantum (RR):", bg=self.bg_color, fg=self.text_color, font=self.font_main)
        self.time_quantum_label.grid(row=5, column=0, pady=5, padx=10, sticky="e")

        self.time_quantum_entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
        self.time_quantum_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")
        self.time_quantum_entry.insert(0, str(self.scheduler.time_quantum))

        self.process_limit_label = tk.Label(self.main_frame, text="Max Processes:", bg=self.bg_color, fg=self.text_color, font=self.font_main)
        self.process_limit_label.grid(row=6, column=0, pady=5, padx=10, sticky="e")

        self.process_limit_entry = tk.Entry(self.main_frame, bg=self.entry_color, fg=self.text_color, font=self.font_main)
        self.process_limit_entry.grid(row=6, column=1, pady=5, padx=10, sticky="w")
        self.process_limit_entry.insert(0, str(self.scheduler.process_limit))

    def _create_buttons(self):
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add Process", bg=self.button_color, fg=self.text_color,
                                    font=self.font_main, width=15, command=self.add_process)
        self.add_button.grid(row=0, column=0, padx=5)

        self.schedule_button = tk.Button(button_frame, text="Schedule", bg=self.button_color, fg=self.text_color,
                                         font=self.font_main, width=15, command=self.schedule)
        self.schedule_button.grid(row=0, column=1, padx=5)

        self.visualize_button = tk.Button(button_frame, text="Gantt Chart", bg=self.button_color, fg=self.text_color,
                                          font=self.font_main, width=15, command=self.visualize_gantt_chart)
        self.visualize_button.grid(row=0, column=2, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset Scheduler", bg=self.button_color, fg=self.text_color,
                                      font=self.font_main, width=15, command=self.reset_scheduler)
        self.reset_button.grid(row=0, column=3, padx=5)

    def _create_metrics_display(self):
        tk.Label(self.main_frame, text="Metrics", bg=self.bg_color, fg=self.text_color, font=self.font_main).grid(
            row=8, columnspan=2, pady=10
        )

        self.metrics_text = tk.Text(self.main_frame, height=16, width=90, bg=self.entry_color, fg=self.text_color,
                                    font=("Courier", 10), wrap=tk.WORD)
        self.metrics_text.grid(row=9, column=0, columnspan=2, pady=5, padx=10)

    def add_process(self):
        try:
            # Validate input fields
            for entry in self.entries:
                if not entry.get().strip().isdigit():
                    raise ValueError("All fields must be valid integers.")

            pid, arrival, burst, queue = (int(e.get()) for e in self.entries)

            # Validate queue value
            if queue not in [1, 2, 3]:
                raise ValueError("Queue must be 1, 2, or 3.")

            # Add the process to the scheduler
            process = Process(pid, arrival, burst, queue)
            if self.scheduler.add_process(process):
                messagebox.showinfo("Success", f"Process {pid} added successfully!")
            else:
                messagebox.showerror("Error", "Process limit reached!")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def schedule(self):
        try:
            # Update time quantum and process limit dynamically, or use defaults if fields are empty
            new_time_quantum = int(self.time_quantum_entry.get()) if self.time_quantum_entry.get().strip() else self.scheduler.time_quantum
            new_process_limit = int(self.process_limit_entry.get()) if self.process_limit_entry.get().strip() else self.scheduler.process_limit

            if new_time_quantum <= 0 or new_process_limit <= 0:
                raise ValueError("Time quantum and process limit must be positive integers.")

            self.scheduler.time_quantum = new_time_quantum
            self.scheduler.process_limit = new_process_limit

            if not self.scheduler.high_priority_queue and not self.scheduler.medium_priority_queue \
                    and not self.scheduler.low_priority_queue:
                messagebox.showerror("Scheduling Error", "No processes added. Please add processes first!")
                return

            self.scheduler.schedule_processes()
            self.metrics_text.delete("1.0", tk.END)
            self.metrics_text.insert(tk.END, "PID     Waiting Time     Turnaround Time\n")
            self.metrics_text.insert(tk.END, "---------------------------------------\n")
            for metric in self.scheduler.calculate_metrics():
                self.metrics_text.insert(
                    tk.END, f"{metric['PID']:<8}{metric['Waiting Time']:<16}{metric['Turnaround Time']}\n"
                )

            # Display average metrics
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

        start_times = [p.start_time for p in self.scheduler.completed_processes]
        durations = [p.burst for p in self.scheduler.completed_processes]
        labels = [f"P{p.pid}" for p in self.scheduler.completed_processes]
        priorities = [p.queue for p in self.scheduler.completed_processes]

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

    def reset_scheduler(self):
        self.scheduler.reset_scheduler()
        self.metrics_text.delete("1.0", tk.END)
        for entry in self.entries + [self.time_quantum_entry, self.process_limit_entry]:
            entry.delete(0, tk.END)
        messagebox.showinfo("Reset", "Scheduler reset successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()