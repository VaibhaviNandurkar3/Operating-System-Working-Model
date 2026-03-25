# To simulate the various states of a process and visualize process state transitions during execution in an operating system.
import time
import random

STATES = ["New", "Ready", "Running", "Waiting", "Terminated"]

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.state = "New"
    
    def transition(self, new_state):
        print(f"Process {self.pid}: {self.state} → {new_state}")
        self.state = new_state
        time.sleep(1)  

def simulate_process(pid):
    p = Process(pid)
    
    p.transition("Ready")
    p.transition("Running")
    
   
    if random.choice([True, False]):
        p.transition("Waiting")
        p.transition("Ready")
        p.transition("Running")
    
    p.transition("Terminated")


for i in range(1, 10):
    print(f"\n--- Simulating Process {i} ---")
    simulate_process(i)