# Multilevel Queue CPU Scheduler

## Project Overview

This project demonstrates the implementation of **Multilevel Queue Scheduling**, a crucial CPU scheduling algorithm used in operating systems. It simulates environments where processes are divided into priority groups (queues), each managed by distinct scheduling policies.

### Key Concepts Covered

- **Queue Prioritization**: Allocating processes to queues based on priority.
- **CPU Scheduling Algorithms**:
  - **First-Come, First-Served (FCFS)**: Applied to high and low-priority queues.
  - **Round Robin (RR)**: Applied to medium-priority queues with a configurable time quantum.
- **Performance Metrics**:
  - **Waiting Time (WT)**: Total time a process spends in the ready queue.
  - **Turnaround Time (TAT)**: Total time from process arrival to completion.

---

## Features

1. **Queue Strategies**:
   - **High-Priority Queue**: FCFS scheduling.
   - **Medium-Priority Queue**: Round Robin scheduling.
   - **Low-Priority Queue**: FCFS scheduling.
2. **Idle Time Management**: Ensures efficient CPU utilization.
3. **Reset Functionality**: Clears all queues and metrics.
4. **Gantt Chart Visualization**: Displays task execution in a graphical timeline.
5. **Error Handling**: Validates user inputs and prevents process overflow.
6. **Dynamic Process Limit**:
   - Users can now set the maximum number of processes dynamically (default is 20).
7. **Enhanced Gantt Chart**:
   - Includes color-coded visualization based on process priorities (High, Medium, Low).
   - Displays a legend for clear interpretation.

---

## Summary Table: Scheduling Algorithms

| **Algorithm**               | **Best For**                           | **Worst For**                      | **Key Issue**                |
|-----------------------------|----------------------------------------|-------------------------------------|-----------------------------|
| **Shortest-Job-First (SJF)** | Low turnaround time, batch systems     | Processes with unpredictable burst | Starvation for long jobs    |
| **Priority Scheduling**      | Critical or high-priority processes    | Low-priority processes             | Starvation, priority tuning |
| **Round Robin (RR)**         | Time-sharing, interactive systems      | High overhead systems              | Context switching overhead  |
| **Multilevel Feedback Queue**| Mixed workloads, adaptive systems      | Complex systems                    | Implementation complexity   |
| **Multilevel Queue**         | Distinct priority categories           | Systems requiring flexibility      | Rigidity in queue movement  |
| **First-Come-First-Served (FCFS)** | Simple environments, short workloads   | Mixed workload environments        | Convoy effect               |

---

### Prerequisites

- **Python 3.x**
- Required libraries:
  - `tkinter`: For GUI interaction.
  - `matplotlib`: For Gantt chart visualization.

Install required libraries:

```bash
pip install matplotlib
```

### Steps to Run

1. Ensure the following files are in the same directory:
   - `main.py`
   - `Scheduler.py`
   - `Process.py`
   - `SchedulerGUI.py`
2. Run the project using the following command:

```bash
python main.py
```

---

## GUI Usage

1. **Add Process**:
   - Enter process details: Process ID, Arrival Time, Burst Time, and Queue Priority.
2. **Schedule**:
   - Execute scheduling algorithms to calculate the order of process execution.
3. **Visualize Gantt Chart**:
   - View a graphical representation of the process timeline.
   - Color-coded bars represent process priority.
4. **Reset Scheduler**:
   - Clear all inputs and restart the scheduling process.
5. **Set Custom Parameters**:
   - Configure **Time Quantum** for Round Robin (default is 2).
   - Adjust the **Maximum Process Limit** (default is 20).

---

## Example Scenarios

### **Test Case 1: FCFS Scheduling**

#### Input:

| PID | Arrival Time | Burst Time | Queue |
| --- | ------------ | ---------- | ----- |
| 1   | 0            | 4          | 1     |
| 2   | 2            | 3          | 1     |

#### Execution:

- **P1**: 0 → 4
- **P2**: 4 → 7

#### Metrics:

| PID | Waiting Time | Turnaround Time |
| --- | ------------ | --------------- |
| 1   | 0            | 4               |
| 2   | 2            | 5               |

#### Gantt Chart:

```
| P1 | P2 |
0    4    7
```

### **Test Case 2: Round Robin Scheduling**

#### Input:

| PID | Arrival Time | Burst Time | Queue |
| --- | ------------ | ---------- | ----- |
| 1   | 0            | 5          | 2     |
| 2   | 1            | 6          | 2     |
| 3   | 2            | 4          | 2     |

#### Quantum: 2

#### Execution:

- **P1**: 0 → 2
- **P2**: 2 → 4
- **P3**: 4 → 6
- Alternates until completion.

#### Metrics:

| PID | Waiting Time | Turnaround Time |
| --- | ------------ | --------------- |
| 1   | 6            | 11              |
| 2   | 5            | 12              |
| 3   | 4            | 8               |

---

## Code Highlights

### 1. **Object-Oriented Programming (OOP)**

- **Classes**:
  - `Process`: Represents a single process.
  - `MultiQueueScheduler`: Handles scheduling logic and queues.
- **Encapsulation**: Exposes only necessary methods and hides implementation details.

### 2. **Data Structures**

- **Deques**: Efficiently manage processes in Round Robin scheduling.
- **Lists**: Store and visualize process data.

### 3. **Algorithm Design**

- **FCFS Logic**: Sequential execution based on arrival order.
- **Round Robin Logic**:
  - Tracks remaining burst time.
  - Preempts processes after the time quantum.
- **Metrics Calculation**:
  - `Waiting Time = Finish Time - Arrival Time - Burst Time`
  - `Turnaround Time = Finish Time - Arrival Time`

### 4. **GUI Development**

- **Tkinter**:
  - Handles user input and process management.
  - Provides intuitive buttons for actions like adding processes and scheduling.
- **Error Handling**:
  - Validates inputs and prevents invalid operations.

### 5. **Visualization**

- **Matplotlib**: Generates Gantt charts for process execution timelines with added color coding and a legend.

---

## Acknowledgments

This project was developed to illustrate key concepts in CPU scheduling algorithms as part of an Operating Systems course. Additionally, it served as an opportunity to test and apply my Python skills by implementing these algorithms, showcasing both programming and algorithmic knowledge in a practical context.
