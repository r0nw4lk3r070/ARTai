import tkinter as tk

class ContentModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.content_box = tk.Text(self.frame, wrap=tk.WORD)
        self.content_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, bd=1, relief="solid", highlightbackground=edge, highlightthickness=1)
        self.content_box.configure(bg=bg, fg=fg, insertbackground=fg)