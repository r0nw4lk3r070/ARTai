import tkinter as tk

class AITab:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent)
        self.ai_box = tk.Text(self.frame, height=40, width=40)
        self.ai_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_theme(self, bg, fg, code_fg, edge):
        self.frame.configure(bg=bg)
        self.ai_box.configure(bg=bg, fg=fg, insertbackground=fg)