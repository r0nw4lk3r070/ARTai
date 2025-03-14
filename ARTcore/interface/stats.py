import tkinter as tk
import os
import time
import psutil
import requests

class StatsModule:
    def __init__(self, parent, art_instance, report_generator):
        self.art = art_instance
        self.report_generator = report_generator
        self.frame = tk.Frame(parent, bd=1, relief="solid")
        self.frame.place(x=10, y=50, width=300, height=950)
        self.nano_balance = 0.0
        self.nano_cost = 0.0
        self.grok_cost = 0.0
        self.stats_values = {}
        self.stats_labels = {}
        self.create_stats_display()
        self.update_balance()  # Initial balance check
        self.update_stats()

    def create_stats_display(self):
        self.main_container = tk.Frame(self.frame, bg="#1A1A1A")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.left_frame = tk.Frame(self.main_container, bg="#1A1A1A")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.right_frame = tk.Frame(self.main_container, bg="#1A1A1A")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        system_stats = [
            ("API Mode", lambda: self.art.core.mode.upper()),
            ("Health", lambda: "Online" if self.art.core.is_active() else "Offline"),
            ("Uptime", lambda: time.strftime("%H:%M:%S", time.gmtime(int(time.time() - self.art.core.start_time)))),
            ("Memory", lambda: f"{psutil.virtual_memory().used / (1024 ** 2):.0f} MB"),
            ("CPU", lambda: f"{psutil.cpu_percent(interval=None):.1f}%")
        ]
        
        data_stats = [
            ("DB Size", lambda: f"{self.get_dir_size(os.path.join(self.art.root_dir, 'ART_DB')) / (1024 ** 3):.5f} GB"),
            ("Project Size", lambda: f"{self.get_dir_size(self.art.root_dir) / (1024 ** 3):.5f} GB"),
            ("File Count", lambda: str(sum(len(files) for _, _, files in os.walk(self.art.root_dir)))),
            ("Datasets", lambda: str(self.art.core._get_dataset_count()))
        ]
        
        cost_stats = [
            ("Nano Balance", lambda: f"{self.nano_balance:.4f} XNO"),
            ("Nano Cost/Prompt", lambda: f"{self.nano_cost:.6f} XNO"),
            ("Grok Cost/Prompt", lambda: f"{self.grok_cost:.6f} USD"),
            ("Grok Total", lambda: f"{self.grok_cost * 10:.2f} USD")
        ]

        for label, value_func in system_stats:
            tk.Label(self.left_frame, text=label + ":", bg="#1A1A1A", fg="#FFFDD0").pack(anchor="w")
            self.stats_labels[label] = tk.Label(self.left_frame, text=value_func(), bg="#1A1A1A", fg="#FFFDD0")
            self.stats_labels[label].pack(anchor="w")
            self.stats_values[label] = value_func

        tk.Label(self.left_frame, text="", bg="#1A1A1A").pack(anchor="w")
        self.grok_button = tk.Label(self.left_frame, text="[Grok]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.grok_button.pack(anchor="w", pady=2)
        self.grok_button.bind("<Button-1>", lambda e: self.switch_mode("grok"))
        self.nanogpt_button = tk.Label(self.left_frame, text="[NanoGPT]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.nanogpt_button.pack(anchor="w", pady=2)
        self.nanogpt_button.bind("<Button-1>", lambda e: self.switch_mode("nanogpt"))

        for label, value_func in data_stats:
            tk.Label(self.right_frame, text=label + ":", bg="#1A1A1A", fg="#FFFDD0").pack(anchor="w")
            self.stats_labels[label] = tk.Label(self.right_frame, text=value_func(), bg="#1A1A1A", fg="#FFFDD0")
            self.stats_labels[label].pack(anchor="w")
            self.stats_values[label] = value_func

        tk.Label(self.right_frame, text="", bg="#1A1A1A").pack(anchor="w")
        for label, value_func in cost_stats:
            tk.Label(self.right_frame, text=label + ":", bg="#1A1A1A", fg="#FFFDD0").pack(anchor="w")
            self.stats_labels[label] = tk.Label(self.right_frame, text=value_func(), bg="#1A1A1A", fg="#FFFDD0")
            self.stats_labels[label].pack(anchor="w")
            self.stats_values[label] = value_func

        tk.Label(self.right_frame, text="", bg="#1A1A1A").pack(anchor="w")
        self.offline_button = tk.Label(self.right_frame, text="[Offline]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.offline_button.pack(anchor="w", pady=2)
        self.offline_button.bind("<Button-1>", lambda e: self.switch_mode("offline"))
        self.balance_button = tk.Label(self.right_frame, text="[Check Balance]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.balance_button.pack(anchor="w", pady=5)
        self.balance_button.bind("<Button-1>", lambda e: self.update_balance())
        self.backup_button = tk.Label(self.right_frame, text="[Watchdog Backup]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.backup_button.pack(anchor="w", pady=5)
        self.backup_button.bind("<Button-1>", lambda e: self.art.watchdog.backup())
        self.report_button = tk.Label(self.right_frame, text="[Report]", cursor="hand2", bg="#1A1A1A", fg="#FFFDD0")
        self.report_button.pack(anchor="w", pady=5)
        self.report_button.bind("<Button-1>", lambda e: self.generate_full_report())

    def switch_mode(self, mode):
        self.art.core._switch_mode(mode)
        self.update_stats()
        print(f"Switched to {mode} mode")

    def update_balance(self):
        if self.art.api_keys.get("nano_gpt"):
            try:
                balance_info = self.art.core.llm_integration.get_balance()
                if balance_info:
                    self.nano_balance = float(balance_info.get("balance", 0.0))
                    self.nano_cost = 0.001  # Placeholder—NanoGPT gives real cost in response
                    print(f"NanoGPT Balance updated: {self.nano_balance:.4f} XNO")
            except Exception as e:
                print(f"Failed to update NanoGPT balance: {e}")
                self.nano_balance = 0.0
                self.nano_cost = 0.0
        self.update_stats_once()

    def update_stats(self):
        for label, value_func in self.stats_values.items():
            self.stats_labels[label].configure(text=value_func())
        self.frame.after(1000, self.update_stats)

    def update_stats_once(self):
        for label, value_func in self.stats_values.items():
            self.stats_labels[label].configure(text=value_func())

    def get_dir_size(self, path):
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                file_path = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(file_path)
                except (FileNotFoundError, PermissionError):
                    continue
        return total

    def generate_full_report(self):
        report_path = self.report_generator.generate_full_report()
        print(f"Report generated at {report_path}")
        return f"Report saved to {report_path}"

    def update_theme(self, bg, fg, edge):
        self.frame.configure(bg=bg, highlightbackground=edge, highlightthickness=1)
        self.main_container.configure(bg=bg)
        self.left_frame.configure(bg=bg)
        self.right_frame.configure(bg=bg)
        for widget in self.left_frame.winfo_children() + self.right_frame.winfo_children():
            widget.configure(bg=bg, fg=fg)