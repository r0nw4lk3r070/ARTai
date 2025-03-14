# ... [rest unchanged]
import os
from dotenv import load_dotenv
from ARTcore.config import load_config
from ARTcore.art_core import ARTCore
from ARTchain.watchdog_core import Watchdog
import tkinter as tk
from tkinter import messagebox
from ARTcore.interface.interface import Interface
import requests
from settings import ROOT_DIR, ENV_PATH, API_KEYS

class ART:
    def __init__(self):
        self.name = "ART"
        self.root_dir = ROOT_DIR
        print(f"Loading .env from: {ENV_PATH}")
        load_dotenv(dotenv_path=ENV_PATH)
        self.api_keys = {k: os.getenv(v) for k, v in API_KEYS.items()}
        print("Loaded API keys:")
        for key, value in self.api_keys.items():
            print(f"{key}: {'Set' if value else 'Not set'}")
        
        self.config = load_config()
        if self.api_keys["nano_gpt"]:
            self.config["preferred_mode"] = "nanogpt"
            print("Setting preferred mode to: nanogpt (NanoGPT API available)")
        elif self.api_keys["grok_api"]:
            self.config["preferred_mode"] = "grok"
            print("Setting preferred mode to: grok (XAI API available)")
        else:
            self.config["preferred_mode"] = "offline"
            print("Setting preferred mode to: offline (No APIs available)")
        
        self.core = ARTCore(self.root_dir, self.config, self.api_keys)
        watchlist_path = os.path.join(self.root_dir, "ARTchain", "watchlist.json")
        if not os.path.exists(watchlist_path):  # Fix: Create if missin'
            with open(watchlist_path, 'w') as f:
                f.write('[]')
            print(f"Created empty watchlist at {watchlist_path}")
        self.watchdog = Watchdog(
            self.root_dir,
            os.path.join(self.root_dir, "ARTchain", "backups"),
            watchlist_path
        )
        self.weather_data = self.fetch_weather("Sint-Joris-Weert")

    # ... [rest unchanged]

    def respond(self, command):
        print(f"{self.name} heard: '{command}'")
        if command.lower() == "watchdog backup":
            self.watchdog.backup()
            return "Watchdog backup completed"
        # ... [rest unchanged]