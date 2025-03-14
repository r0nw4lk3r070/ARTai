import tkinter as tk
from .chat import ChatModule
from .stats import StatsModule
from settings import THEME, CHAT_FONT  # Absolute import

class Interface:
    def __init__(self, root, art_instance, report_generator):
        self.root = root
        self.art = art_instance
        self.report_generator = report_generator
        self.root.title("ART Interface")
        self.root.geometry("1280x1024")
        self.root.configure(bg=THEME["bg"])

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=THEME["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Chat module
        self.chat_module = ChatModule(self.main_frame, self.art)
        self.chat_module.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Stats module
        self.stats_module = StatsModule(self.main_frame, self.art, self.report_generator)

        # Weather label
        self.weather_label = tk.Label(self.main_frame, text=self.art.weather_data, bg=THEME["bg"], fg=THEME["fg"], font=("Arial", 12))
        self.weather_label.pack(side=tk.TOP, anchor="ne", padx=5, pady=5)

        self.update_theme()

    def update_weather(self):
        self.weather_label.config(text=self.art.weather_data)
        self.root.after(60000, self.update_weather)

    def update_theme(self):
        bg = THEME["bg"]
        fg = THEME["fg"]
        edge = THEME["edge"]
        self.main_frame.configure(bg=bg)
        self.chat_module.update_theme(bg, fg, edge)
        self.stats_module.update_theme(bg, fg, edge)
        self.weather_label.configure(bg=bg, fg=fg)