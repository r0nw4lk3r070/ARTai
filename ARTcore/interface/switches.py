import tkinter as tk

class SwitchesModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent)
        self.api_var = tk.StringVar(value="Offline")
        tk.Radiobutton(self.frame, text="Grok", variable=self.api_var, value="Grok").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame, text="Nano GPT", variable=self.api_var, value="Nano GPT").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame, text="Offline", variable=self.api_var, value="Offline").pack(side=tk.LEFT)