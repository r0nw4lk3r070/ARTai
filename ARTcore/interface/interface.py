# Restored from ART Watchdog backup - Updated 2025-03-13
import tkinter as tk
from tkinter import ttk
from ARTcore.interface.chat import ChatModule
from ARTcore.interface.content import ContentModule
from ARTcore.interface.stats import StatsModule

class Interface:
    def __init__(self, root, art_instance):
        self.root = root
        self.art = art_instance
        self.root.title("ART - Pirate Command")
        self.root.geometry("1400x1000")
        self.bg_color = "#1A1A1A"
        self.fg_color = "#FFFDD0"  # Cream white text
        self.edge_color = "#4B0082"  # Night purple edges

        total_width = 1400
        total_height = 1000
        stats_width = 300
        module_height = (total_height - 90) / 2

        self.art_label = tk.Label(self.root, text="ART", bg=self.bg_color, fg=self.fg_color, font=("Arial", 14))
        self.art_label.place(x=10, y=10)
        self.weather_label = tk.Label(self.root, text=self.art.weather_data, bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.weather_label.place(relx=1.0, y=10, anchor="ne", x=-10)

        self.stats = StatsModule(self.root, self.art)
        self.stats.frame.place(x=10, y=50, width=stats_width, height=total_height - 90)

        self.content = ContentModule(self.root, self.art)
        self.content.frame.place(x=10 + stats_width + 20, y=50, width=total_width - stats_width - 40, height=module_height)

        self.chat = ChatModule(self.root, self.art)
        self.chat.frame.place(x=10 + stats_width + 20, y=50 + module_height, width=total_width - stats_width - 40, height=module_height)

        self.root.configure(bg=self.bg_color)
        self.content.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.chat.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.stats.update_theme(self.bg_color, self.fg_color, self.edge_color)

        self.root.bind("<Configure>", self.on_resize)
        self.root.after(60000, self.update_weather)

    def update_weather(self):
        self.weather_label.config(text=self.art.weather_data)
        self.root.after(60000, self.update_weather)

    def on_resize(self, event):
        total_width = self.root.winfo_width()
        total_height = self.root.winfo_height()
        stats_width = 300
        module_height = max((total_height - 90) / 2, 100)

        self.weather_label.place(relx=1.0, y=10, anchor="ne", x=-10)
        self.stats.frame.place(x=10, y=50, width=stats_width, height=total_height - 90)
        self.content.frame.place(x=10 + stats_width + 20, y=50, width=total_width - stats_width - 40, height=module_height)
        self.chat.frame.place(x=10 + stats_width + 20, y=50 + module_height, width=total_width - stats_width - 40, height=module_height)