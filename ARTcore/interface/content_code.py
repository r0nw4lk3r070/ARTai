import tkinter as tk

class CodeTab:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent)
        self.code_box = tk.Text(self.frame, height=40, width=40)
        self.code_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_theme(self, bg, fg, code_fg, edge):
        self.frame.configure(bg=bg)
        self.code_box.configure(bg=bg, fg=code_fg["code"], insertbackground=fg)