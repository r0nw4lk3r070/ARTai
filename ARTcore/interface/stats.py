# Stats - Balance Cached - 2025-03-14
import tkinter as tk
import os
import time
import psutil

class StatsModule:
    def __init__(self, parent, art_instance):
        self.art = art_instance
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.stats_box = tk.Text(self.frame, height=22, wrap=tk.WORD, font=("Arial", 12))
        self.stats_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.todo_box = tk.Text(self.frame, height=22, wrap=tk.WORD, font=("Arial", 12))
        self.todo_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.nano_balance = 0.0
        self.nano_cost = 0.0
        self.grok_cost = 0.0
        self.update_balance()  # Initial fetch
        self.update_stats()

    def update_stats(self):
        self.stats_box.delete(1.0, tk.END)
        self.stats_box.insert(tk.END, f"ART Health: {'Online' if self.art.core.is_active() else 'Offline'}\n")
        self.stats_box.insert(tk.END, f"API: {self.art.core.mode.upper()}\n")
        self.stats_box.insert(tk.END, f"DB Size: {self.get_dir_size(os.path.join(self.art.root_dir, 'ART_DB')) / (1024 ** 3):.5f} GB\n")
        self.stats_box.insert(tk.END, f"Project Size: {self.get_dir_size(self.art.root_dir) / (1024 ** 3):.2f} GB\n")
        self.stats_box.insert(tk.END, f"Run Time: {time.strftime('%H:%M:%S', time.gmtime(int(time.time() - self.art.core.start_time)))}\n")
        self.stats_box.insert(tk.END, f"File Count: {sum(len(files) for _, _, files in os.walk(self.art.root_dir))}\n")
        self.stats_box.insert(tk.END, f"Grok Cost: ${self.grok_cost:.2f}\n")
        self.stats_box.insert(tk.END, f"NanoGPT Balance: {self.nano_balance:.4f} XNO\n")
        self.stats_box.insert(tk.END, "[Watchdog Backup]\n", "button")
        self.stats_box.insert(tk.END, "[Check Balance]\n", "button")
        self.stats_box.tag_config("button", foreground="#00FFFF")
        self.stats_box.bind("<Button-1>", self.handle_click)
        self.frame.after(1000, self.update_stats)

    def handle_click(self, event):
        line = self.stats_box.index(f"@{event.x},{event.y} linestart")
        text = self.stats_box.get(line, f"{line} lineend")
        if "[Watchdog Backup]" in text:
            self.art.watchdog.backup()
            self.stats_box.insert(tk.END, "Backup triggered!\n")
        elif "[Check Balance]" in text:
            self.update_balance()
            self.stats_box.insert(tk.END, "Balance updated!\n")

    def update_balance(self):
        balance_info = self.art.core.get_balance()
        if balance_info and "balance" in balance_info:
            self.nano_balance = float(balance_info["balance"])
            self.nano_cost = 0.001  # Placeholder
        else:
            self.nano_balance = self.nano_balance if self.nano_balance else 0.0
            self.nano_cost = 0.0

    def get_dir_size(self, path):
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, f))
                except (FileNotFoundError, PermissionError):
                    continue
        return total

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.stats_box.configure(bg=bg, fg=fg, insertbackground=fg)
        self.todo_box.configure(bg=bg, fg=fg, insertbackground=fg)