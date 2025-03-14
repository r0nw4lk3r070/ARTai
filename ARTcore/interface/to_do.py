import tkinter as tk

class ToDoModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, width=400, height=300)
        self.todo_list = tk.Text(self.frame, height=30, width=40)  # Doubled height
        self.todo_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.frame.pack_propagate(False)

    def update_theme(self, bg, fg, code_fg, edge):
        self.frame.configure(bg=bg)
        self.todo_list.configure(bg=bg, fg=fg, insertbackground=fg)