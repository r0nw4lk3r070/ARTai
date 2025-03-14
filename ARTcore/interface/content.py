import tkinter as tk
from tkinter import ttk

class ContentModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.content_area = tk.Frame(self.frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tab_contents = {}
        for name in ["CLI", "Code", "Mail", "Chat", "Web", "News"]:
            self.tab_contents[name] = tk.Text(self.content_area, wrap=tk.WORD)

        self.active_tab = "CLI"
        self.tab_contents[self.active_tab].pack(fill=tk.BOTH, expand=True)

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
            self.tab_contents[self.active_tab].pack_forget()
        self.tab_contents[tab_name].pack(fill=tk.BOTH, expand=True)
        self.active_tab = tab_name
        for name, btn in self.tab_buttons.items():
            btn.configure(bg="#000000" if name != tab_name else "#333333")

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, bd=1, relief="solid", highlightbackground=edge, highlightthickness=1)
        self.content_area.configure(bg=bg)
        self.tab_bar.configure(bg="#000000")
        for btn in self.tab_buttons.values():
            btn.configure(bg="#000000" if btn.cget("text") != self.active_tab else "#333333", fg="#FFFFFF")
        for tab in self.tab_contents.values():
            tab.configure(bg=bg, fg=fg, insertbackground=fg)