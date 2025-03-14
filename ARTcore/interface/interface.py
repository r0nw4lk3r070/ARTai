# Interface - API Slim - 2025-03-14
import tkinter as tk
from ARTcore.interface.stats import StatsModule
from ARTcore.interface.content import ContentModule

class ARTInterface:
    def __init__(self, root, art_instance):
        self.root = root
        self.art = art_instance
        self.root_dir = self.art.root_dir
        self.core = self.art  # ART is core now
        self.root.title("ART")
        self.root.geometry("1400x1000")
        self.stats_module = StatsModule(self.root, self)
        self.content_module = ContentModule(self.root, self)
        self.stats_module.frame.place(x=10, y=50, width=300, height=910)
        self.content_module.frame.place(x=330, y=50, width=1060, height=455)
        print("Interface created.")