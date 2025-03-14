# Restored from ART Watchdog backup - Role swapped to Content 2025-03-14
import tkinter as tk
from tkinter import ttk

class ChatModule:  # Now acts as Content
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.content_area = tk.Frame(self.frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tab_contents = {}
        self.tab_inputs = {}
        for name in ["CLI", "Code", "Mail", "Chat", "Web", "News"]:
            tab_frame = tk.Frame(self.content_area)
            text = tk.Text(tab_frame, wrap=tk.WORD, height=20, font=("Arial", 12))
            text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.tab_contents[name] = text
            if name == "CLI":
                input_box = tk.Entry(tab_frame, bd=1, relief="solid", font=("Arial", 12))
                input_box.pack(fill=tk.X, padx=5, pady=5)
                input_box.bind("<Return>", lambda e: self.send_cli_command())
                self.tab_inputs[name] = input_box

        self.active_tab = "CLI"
        self.tab_contents[self.active_tab].master.pack(fill=tk.BOTH, expand=True)

        self.tab_bar = tk.Frame(self.frame, bg="#000000")
        self.tab_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tab_buttons = {}
        for name in self.tab_contents.keys():
            btn = tk.Label(self.tab_bar, text=name, bg="#000000", fg="#FFFFFF", padx=20, pady=5, cursor="hand2")
            btn.pack(side=tk.LEFT)
            btn.bind("<Button-1>", lambda e, n=name: self.switch_tab(n))
            self.tab_buttons[name] = btn
            
        self.tab_buttons["CLI"].configure(bg="#333333")

    def switch_tab(self, tab_name):
        if self.active_tab:
            self.tab_contents[self.active_tab].master.pack_forget()
        
        self.tab_contents[tab_name].master.pack(fill=tk.BOTH, expand=True)
        self.active_tab = tab_name
        
        for name, btn in self.tab_buttons.items():
            btn.configure(bg="#000000" if name != tab_name else "#333333")

    def send_cli_command(self):
        if self.active_tab == "CLI" and "CLI" in self.tab_inputs:
            command = self.tab_inputs["CLI"].get().strip()
            if command:
                self.tab_contents["CLI"].insert(tk.END, f"> {command}\n")
                response = self.art.respond(command)
                self.tab_contents["CLI"].insert(tk.END, f"ART: {response}\n\n")
                self.tab_contents["CLI"].see(tk.END)
                self.tab_inputs["CLI"].delete(0, tk.END)

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.content_area.configure(bg=bg)
        self.tab_bar.configure(bg="#000000")
        for btn in self.tab_buttons.values():
            btn.configure(bg="#000000" if btn.cget("text") != self.active_tab else "#333333", fg="#FFFFFF")
        for name, tab in self.tab_contents.items():
            tab.configure(bg=bg, fg=fg, insertbackground=fg)
            if name in self.tab_inputs:
                self.tab_inputs[name].configure(bg=bg, fg=fg, insertbackground=fg)