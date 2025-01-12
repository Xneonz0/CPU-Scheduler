# Multilevel Queue CPU Scheduler

## Overview

The Multilevel Queue CPU Scheduler is an advanced project designed to bridge the gap between theory and practical application in operating systems. It implements core scheduling algorithms used in modern CPUs, providing an interactive platform to learn and test these concepts. This project not only serves as an educational tool but also as a testament to my programming skills and ability to translate complex theories into functional, real-world applications.

## Key Features

### Comprehensive Scheduling Support
- **High Priority Queue**: Implements Preemptive Priority Scheduling to handle critical tasks efficiently.
- **Medium Priority Queue**: Uses Round Robin Scheduling with a configurable time quantum to ensure fairness.
- **Low Priority Queue**: Applies Shortest Job First (SJF) for efficient execution of less critical tasks.

### Modern and Intuitive GUI
- Input fields for process attributes (ID, Arrival Time, Burst Time, Queue, Priority).
- Dynamic metrics display for Waiting Time, Turnaround Time, and averages.
- Professional Gantt chart visualization:
  - Color-coded bars for different priority levels.
  - Time markers and a sleek legend for clarity.

### Practical Enhancements
- **Handles Idle CPU Time**: Accurately represents gaps in CPU usage.
- **Error Handling**: Validates user inputs and prevents invalid operations.
- **Customizable Parameters**:
  - Configurable maximum number of processes (default: 20).
  - Adjustable time quantum for Round Robin.
- **Reset Functionality**: Clears all inputs and outputs to start fresh.

## Purpose

This project was developed with two main objectives:
1. **Educational Application**: To demonstrate the theoretical foundations of CPU scheduling algorithms in a visual and interactive manner.
2. **Skill Demonstration**: To showcase my ability to design, implement, and optimize complex algorithms, as well as develop user-friendly software solutions.

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

## Getting Started

### Prerequisites
- **Python 3.x** installed on your system.
- Required libraries:
  - `tkinter` (built-in with Python).
  - `matplotlib` (install using `pip`).

Install `matplotlib` using:
```bash
pip install matplotlib
```

### How to Run
1. Ensure the following files are in the same directory:
   - `main.py`
   - `Scheduler.py`
   - `Process.py`
   - `SchedulerGUI.py`
2. Launch the program using:
```bash
python main.py
```

3. Interact with the GUI:
   - Add processes and define their attributes.
   - Schedule the processes.
   - Visualize the results in the Gantt chart.
   - Reset the scheduler as needed.

---

## Example Usage

### Case 1: High Priority Scheduling (Preemptive Priority)

#### Input:
| PID | Arrival Time | Burst Time | Queue | Priority |
| --- | ------------ | ---------- | ----- | -------- |
| 1   | 0            | 4          | 1     | 1        |
| 2   | 2            | 3          | 1     | 2        |
| 3   | 4            | 5          | 1     | 3        |

#### Output:
| PID | Waiting Time | Turnaround Time |
| --- | ------------ | --------------- |
| 1   | 0            | 4               |
| 2   | 2            | 5               |
| 3   | 3            | 8               |

#### Gantt Chart:
```
| P1 | P2 | P3 |
0    4    7    12
```

---

### Case 2: Medium Priority Scheduling (Round Robin)

#### Input:
| PID | Arrival Time | Burst Time | Queue | Priority |
| --- | ------------ | ---------- | ----- | -------- |
| 1   | 0            | 5          | 2     | 2        |
| 2   | 1            | 6          | 2     | 3        |
| 3   | 2            | 4          | 2     | 2        |

#### Quantum: 2

#### Output:
| PID | Waiting Time | Turnaround Time |
| --- | ------------ | --------------- |
| 1   | 6            | 11              |
| 2   | 5            | 12              |
| 3   | 4            | 8               |

#### Gantt Chart:
```
| P1 | P2 | P3 | P1 | P2 | P3 |
0    2    4    6    8   10   12
```

---

### Case 3: Low Priority Scheduling (Shortest Job First - SJF)

#### Input:
| PID | Arrival Time | Burst Time | Queue | Priority |
| --- | ------------ | ---------- | ----- | -------- |
| 1   | 0            | 8          | 3     | 3        |
| 2   | 1            | 4          | 3     | 2        |
| 3   | 2            | 2          | 3     | 1        |

#### Output:
| PID | Waiting Time | Turnaround Time |
| --- | ------------ | --------------- |
| 1   | 10           | 18              |
| 2   | 5            | 9               |
| 3   | 0            | 2               |

#### Gantt Chart:
```
| P3 | P2 | P1 |
0    2    6    14
```

---

## Project Structure

### Object-Oriented Design
- **Classes**:
  - `Process`: Defines a process with attributes like PID, arrival time, burst time, etc.
  - `MultiQueueScheduler`: Manages the scheduling logic and metrics calculation.
  - `SchedulerGUI`: Provides a graphical interface for user interaction.

### Python Concepts Used
- **Object-Oriented Programming (OOP)**:
  - Encapsulation and separation of concerns using distinct classes for processes, scheduling logic, and GUI.
- **Data Structures**:
  - **Deques**: Used for efficient cycling in Round Robin scheduling.
  - **Lists**: Maintain process queues and sorting for Shortest Job First (SJF).
  - **Dictionaries**: Map priorities to colors for Gantt chart visualization.
- **Data Visualization**:
  - `matplotlib` for professional Gantt chart creation with color-coded bars and legends.
- **Dynamic GUI**:
  - Built with `tkinter`, supporting user interaction for process input, scheduling, and visualization.
- **Error Handling**:
  - Robust input validation with descriptive error messages to ensure smooth operation.
- **Algorithm Design**:
  - Implementation of Preemptive Priority, Round Robin, and SJF algorithms with modular and efficient logic.

### Metrics Calculation
- **Waiting Time (WT)**: `Finish Time - Arrival Time - Burst Time`
- **Turnaround Time (TAT)**: `Finish Time - Arrival Time`

### Visualization
- **Gantt Chart**:
  - Dynamic scaling to handle up to 20 processes.
  - Color-coded bars for High (Red), Medium (Purple), and Low (Green) priorities.
  - A professional legend and time markers for clarity.

---

## Why This Project Stands Out

1. **Educational Value**: Provides an interactive way to learn CPU scheduling.
2. **Practical Application**: Demonstrates real-world scenarios with accurate metrics and visualizations.
3. **Skill Showcase**: Highlights my ability to develop complex algorithms, optimize code, and create user-focused designs.

---

## Acknowledgments

This project reflects my dedication to learning and applying programming concepts to solve meaningful problems. It’s a blend of theory, practice, and creativity, and I hope it inspires others to explore the fascinating field of operating systems.
