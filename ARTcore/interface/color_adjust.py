import tkinter as tk
from tkinter import ttk

class ColorAdjustForm:
    def __init__(self, parent, interface):
        self.interface = interface
        self.frame = tk.Frame(parent, bg="#1A1A1A")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Explanation
        tk.Label(self.frame, text="Adjust ART Colors:", bg="#1A1A1A", fg="#E0E0E0", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.frame, text="Background (bg): Main window color\nForeground (fg): Text color\nEdge: Borders/tabs", bg="#1A1A1A", fg="#E0E0E0").pack(pady=5)

        # Color entries
        self.bg_var = tk.StringVar(value="#1A1A1A")
        self.fg_var = tk.StringVar(value="#E0E0E0")
        self.edge_var = tk.StringVar(value="#4B0082")

        tk.Label(self.frame, text="Background:", bg="#1A1A1A", fg="#E0E0E0").pack()
        tk.Entry(self.frame, textvariable=self.bg_var).pack()

        tk.Label(self.frame, text="Foreground:", bg="#1A1A1A", fg="#E0E0E0").pack()
        tk.Entry(self.frame, textvariable=self.fg_var).pack()

        tk.Label(self.frame, text="Edge:", bg="#1A1A1A", fg="#E0E0E0").pack()
        tk.Entry(self.frame, textvariable=self.edge_var).pack()

        # Buttons
        tk.Button(self.frame, text="Refresh", command=self.refresh).pack(pady=5)
        tk.Button(self.frame, text="Save", command=self.save).pack(pady=5)

    def refresh(self):
        self.interface.bg_color = self.bg_var.get()
        self.interface.fg_color = self.fg_var.get()
        self.interface.edge_color = self.edge_var.get()
        self.interface.root.configure(bg=self.bg_color)
        self.interface.art_label.configure(bg=self.bg_color, fg=self.fg_color)
        self.interface.weather_label.configure(bg=self.bg_color, fg=self.edge_color)
        self.interface.content.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.interface.chat.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.interface.stats.update_theme(self.bg_color, self.fg_color, self.edge_color)

    def save(self):
        # Save to interface.py (manual edit for now)
        with open(r"C:\Users\r0nw4\ART\ARTcore\interface\interface.py", "r") as f:
            lines = f.readlines()
        with open(r"C:\Users\r0nw4\ART\ARTcore\interface\interface.py", "w") as f:
            for line in lines:
                if "self.bg_color =" in line:
                    f.write(f"        self.bg_color = \"{self.bg_var.get()}\"\n")
                elif "self.fg_color =" in line:
                    f.write(f"        self.fg_color = \"{self.fg_var.get()}\"\n")
                elif "self.edge_color =" in line:
                    f.write(f"        self.edge_color = \"{self.edge_var.get()}\"\n")
                else:
                    f.write(line)
        self.refresh()