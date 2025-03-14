import tkinter as tk

class WebModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent)
        self.web_box = tk.Text(self.frame, height=40, width=80)
        self.web_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.web_box.insert(tk.END, "Grok’s Surprise: 'Yar, I be watchin’ ye code from the cosmos!'")
        self.update_theme("#FFFFFF", "#000000", {"code": "#0000CC", "string": "#CC0000"}, "#333333")

    def show(self, url=None):
        self.frame.place(x=300, y=100, width=800, height=800)
        if url:
            self.web_box.delete(1.0, tk.END)
            self.web_box.insert(tk.END, f"Loading {url}... (Web soon!)")

    def hide(self):
        self.frame.place_forget()

    def update_theme(self, bg, fg, code_fg, edge):
        self.frame.configure(bg=bg)
        self.web_box.configure(bg=bg, fg=fg, insertbackground=fg)