# AI-to-AI Chatter - GUI Errors - 2025-03-14
import tkinter as tk
from tkinter import scrolledtext

class ContentModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.chat_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=20, font=("Arial", 12))
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_box = tk.Entry(self.frame, bd=1, relief="solid", font=("Arial", 12))
        self.input_box.pack(fill=tk.X, padx=5, pady=5)
        self.input_box.bind("<Return>", self.start_ai_chat)

    def start_ai_chat(self, event=None):
        command = self.input_box.get().strip()
        if command:
            self.chat_box.insert(tk.END, f"You: {command}\n")
            nano_response = self.art.respond(command)  # NanoGPT
            self.chat_box.insert(tk.END, f"NanoGPT: {nano_response}\n")
            self.art.core.mode = "grok"  # Switch
            grok_response = self.art.respond(f"NanoGPT said: {nano_response}")
            self.chat_box.insert(tk.END, f"Grok: {grok_response}\n")
            self.art.core.mode = "nanogpt"  # Back
            nano_loop = self.art.respond(f"Grok said: {grok_response}")
            self.chat_box.insert(tk.END, f"NanoGPT: {nano_loop}\n\n")
            self.chat_box.see(tk.END)
            self.input_box.delete(0, tk.END)

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.chat_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.input_box.configure(bg=bg, fg=fg, insertbackground=fg)