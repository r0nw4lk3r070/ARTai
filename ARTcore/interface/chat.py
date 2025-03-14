import tkinter as tk
from tkinter import scrolledtext

class ChatModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.chat_display = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=20, width=80, font=("Arial", 14))  # Font 14
        self.chat_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.input_frame = tk.Frame(self.frame)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.command_entry = tk.Entry(self.input_frame, font=("Arial", 14))  # Match font
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.send_command)
        
        self.send_button = tk.Label(self.input_frame, text="[Send]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0", font=("Arial", 14))
        self.send_button.pack(side=tk.RIGHT, padx=5)
        self.send_button.bind("<Button-1>", self.send_command)

    def send_command(self, event=None):
        command = self.command_entry.get().strip()
        if command:
            self.chat_display.insert(tk.END, f"You: {command}\n")
            response = self.art.respond(command)
            self.chat_display.insert(tk.END, f"ART: {response}\n\n")
            self.chat_display.see(tk.END)
            self.command_entry.delete(0, tk.END)

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.chat_display.configure(bg=bg, fg=fg)
        self.input_frame.configure(bg=bg)
        self.command_entry.configure(bg=bg, fg=fg)
        self.send_button.configure(bg=bg, fg=fg)