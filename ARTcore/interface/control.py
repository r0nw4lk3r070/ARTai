import tkinter as tk

class ControlModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, width=400)
        self.label = tk.Label(self.frame, text="Control Panel - Coming Soon!")
        self.label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)