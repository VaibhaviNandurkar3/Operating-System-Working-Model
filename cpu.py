import tkinter as tk
import random
import time
import threading
from datetime import datetime
import winsound  # for sound effects on Windows

# Define process states and transitions
states = ["New", "Ready", "Running", "Waiting", "Terminated"]

transitions = {
    "New": ["Ready"],
    "Ready": ["Running", "Waiting"],
    "Running": ["Ready", "Waiting", "Terminated"],
    "Waiting": ["Ready"],
    "Terminated": []
}

# Colors for each state
state_colors = {
    "New": "skyblue",
    "Ready": "orange",
    "Running": "lightgreen",
    "Waiting": "yellow",
    "Terminated": "red"
}

class ProcessSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative Process Management Simulator")

        self.current_state = "New"
        self.running = False
        self.transition_count = 0
        self.start_time = None

        # Main frame with pista background
        main_frame = tk.Frame(root, bg="#C1E1C1")
        main_frame.pack(fill="both", expand=True)

        # Canvas for diagram
        self.canvas = tk.Canvas(main_frame, width=500, height=500, bg="#C1E1C1")
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        # Dashboard panel
        dashboard = tk.Frame(main_frame, bg="#E6FFE6", relief="ridge", bd=4)
        dashboard.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        tk.Label(dashboard, text="📊 Dashboard", font=("Arial", 16, "bold"), bg="#E6FFE6").pack(pady=10)

        self.state_label = tk.Label(dashboard, text=f"Current State: {self.current_state}",
                                    font=("Arial", 14), fg="blue", bg="#E6FFE6")
        self.state_label.pack(pady=5)

        self.counter_label = tk.Label(dashboard, text=f"Transitions: {self.transition_count}",
                                      font=("Arial", 14), fg="darkgreen", bg="#E6FFE6")
        self.counter_label.pack(pady=5)

        self.time_label = tk.Label(dashboard, text="Elapsed Time: 0s",
                                   font=("Arial", 14), fg="purple", bg="#E6FFE6")
        self.time_label.pack(pady=5)

        # Control buttons
        frame = tk.Frame(dashboard, bg="#E6FFE6")
        frame.pack(pady=10)

        self.start_button = tk.Button(frame, text="Auto Simulation", command=self.start_simulation, font=("Arial", 12))
        self.start_button.grid(row=0, column=0, padx=5)

        self.step_button = tk.Button(frame, text="Step Forward", command=self.step_forward, font=("Arial", 12))
        self.step_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(frame, text="Reset", command=self.reset_simulation, font=("Arial", 12))
        self.reset_button.grid(row=0, column=2, padx=5)

        # Text box to log transitions
        self.log_box = tk.Text(dashboard, height=15, width=40, font=("Arial", 12), bg="#F0FFF0")
        self.log_box.pack(pady=10)

        # Legend box
        legend = tk.Label(dashboard, text="Legend:\nNew=SkyBlue | Ready=Orange | Running=LightGreen | Waiting=Yellow | Terminated=Red",
                          font=("Arial", 10), bg="#E6FFE6", fg="black", justify="left")
        legend.pack(pady=5)

        # Positions for each state circle
        self.positions = {
            "New": (100, 100),
            "Ready": (250, 100),
            "Running": (400, 100),
            "Waiting": (250, 250),
            "Terminated": (250, 400)
        }

        # Draw states
        self.state_nodes = {}
        for state, (x, y) in self.positions.items():
            node = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill="lightgray", outline="black", width=2)
            self.canvas.create_text(x, y, text=state, font=("Arial", 12))
            self.state_nodes[state] = node

        # Draw transitions (arrows)
        self.arrows = {}
        for state, next_states in transitions.items():
            x1, y1 = self.positions[state]
            for next_state in next_states:
                x2, y2 = self.positions[next_state]
                arrow = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="black", width=2)
                self.arrows[(state, next_state)] = arrow

        # Highlight initial state
        self.highlight_state("New")

    def highlight_state(self, state):
        for s, node in self.state_nodes.items():
            self.canvas.itemconfig(node, fill="lightgray", width=2)
        self.canvas.itemconfig(self.state_nodes[state], fill=state_colors[state], width=4)

    def animate_arrow(self, from_state, to_state):
        arrow = self.arrows.get((from_state, to_state))
        if arrow:
            for _ in range(2):
                self.canvas.itemconfig(arrow, fill="red", width=3)
                self.canvas.update()
                time.sleep(0.2)
                self.canvas.itemconfig(arrow, fill="black", width=2)
                self.canvas.update()
                time.sleep(0.2)

    def play_sound(self):
        winsound.Beep(800, 200)

    def log_transition(self, new_state):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{timestamp}] Transition: {self.current_state} → {new_state}\n")
        self.log_box.see(tk.END)

    def update_state(self, new_state):
        self.animate_arrow(self.current_state, new_state)
        self.play_sound()
        self.log_transition(new_state)
        self.current_state = new_state
        self.transition_count += 1
        self.state_label.config(text=f"Current State: {self.current_state}")
        self.counter_label.config(text=f"Transitions: {self.transition_count}")
        self.highlight_state(new_state)

    def update_time(self):
        if self.start_time and self.running:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Elapsed Time: {elapsed}s")
            self.root.after(1000, self.update_time)

    def simulate(self):
        self.running = True
        self.start_time = time.time()
        self.update_time()
        while self.current_state != "Terminated" and self.running:
            possible_next = transitions[self.current_state]
            if not possible_next:
                break
            next_state = random.choice(possible_next)
            self.update_state(next_state)
            time.sleep(1)
        self.running = False
        self.log_box.insert(tk.END, "Process finished execution.\n")

    def start_simulation(self):
        if not self.running:
            threading.Thread(target=self.simulate).start()

    def step_forward(self):
        if self.current_state == "Terminated":
            self.log_box.insert(tk.END, "Process already terminated. Reset to start again.\n")
            return
        if not self.start_time:
            self.start_time = time.time()
            self.update_time()
        possible_next = transitions[self.current_state]
        if possible_next:
            next_state = random.choice(possible_next)
            self.update_state(next_state)
        else:
            self.log_box.insert(tk.END, "No further transitions available.\n")

    def reset_simulation(self):
        self.running = False
        self.current_state = "New"
        self.transition_count = 0
        self.start_time = None
        self.state_label.config(text=f"Current State: {self.current_state}")
        self.counter_label.config(text=f"Transitions: {self.transition_count}")
        self.time_label.config(text="Elapsed Time: 0s")
        self.log_box.delete(1.0, tk.END)
        self.highlight_state("New")
        self.log_box.insert(tk.END, "Simulation reset.\n")


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#C1E1C1")
    app = ProcessSimulatorGUI(root)
    root.mainloop()