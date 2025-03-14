# Cemented Interface - Locked 2025-03-14 - AI Chatter Top, Chat Bottom
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
        self.fg_color = "#FFFDD0"
        self.edge_color = "#4B0082"

        stats_x, stats_y, stats_width, stats_height = 10, 50, 300, 910
        content_x, content_y, content_width, content_height = 330, 50, 1060, 455
        chat_x, chat_y, chat_width, chat_height = 330, 505, 1060, 455

        print(f"Stats locked at x={stats_x}, y={stats_y}, width={stats_width}, height={stats_height}")
        print(f"Content (AI chatter) locked at x={content_x}, y={content_y}, width={content_width}, height={content_height}")
        print(f"Chat locked at x={chat_x}, y={chat_y}, width={chat_width}, height={chat_height}")

        self.art_label = tk.Label(self.root, text="ART", bg=self.bg_color, fg=self.fg_color, font=("Arial", 14))
        self.art_label.place(x=10, y=10)
        self.weather_label = tk.Label(self.root, text=self.art.weather_data, bg=self.bg_color, fg=self.fg_color, font=("Arial", 12))
        self.weather_label.place(x=1350, y=10, anchor="ne")

        self.stats = StatsModule(self.root, self.art)
        self.stats.frame.place(x=stats_x, y=stats_y, width=stats_width, height=stats_height)

        self.content = ContentModule(self.root, self.art)  # Top-right - AI-to-AI
        self.content.frame.place(x=content_x, y=content_y, width=content_width, height=content_height)

        self.chat = ChatModule(self.root, self.art)  # Bottom-right - User chat
        self.chat.frame.place(x=chat_x, y=chat_y, width=chat_width, height=chat_height)

        self.root.configure(bg=self.bg_color)
        self.content.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.chat.update_theme(self.bg_color, self.fg_color, self.edge_color)
        self.stats.update_theme(self.bg_color, self.fg_color, self.edge_color)

        self.root.after(60000, self.update_weather)

    def update_weather(self):
        self.weather_label.config(text=self.art.weather_data)
        self.root.after(60000, self.update_weather)