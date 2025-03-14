# Restored from ART Watchdog backup - Role swapped to Chat 2025-03-14
import tkinter as tk
from tkinter import scrolledtext

class ContentModule:  # Now acts as Chat
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.chat_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=20, font=("Arial", 14))
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_box = tk.Entry(self.frame, bd=1, relief="solid", font=("Arial", 14))
        self.input_box.pack(fill=tk.X, padx=5, pady=8)
        self.input_box.bind("<Return>", self.send_command)

    def send_command(self, event=None):
        command = self.input_box.get().strip()
        if command:
            self.chat_box.insert(tk.END, f"You: {command}\n")
            response = self.art.respond(command)
            self.chat_box.insert(tk.END, f"ART: {response}\n\n")
            self.chat_box.see(tk.END)
            self.input_box.delete(0, tk.END)

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.chat_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.input_box.configure(bg=bg, fg=fg, insertbackground=fg)