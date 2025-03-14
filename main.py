# Debug Mode - AI-to-AI Ready - 2025-03-14
import os
import sys
import traceback
print("Starting imports...")
try:
    from dotenv import load_dotenv
    from ARTcore.config import load_config
    from ARTcore.art_core import ARTCore
    from ARTchain.watchdog_core import Watchdog
    import tkinter as tk
    from tkinter import messagebox
    from ARTcore.interface.interface import Interface
    import requests
    from settings import ROOT_DIR, ENV_PATH, API_KEYS
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

print("Imports done, defining ART...")

class ART:
    def __init__(self):
        print("ART init started...")
        self.name = "ART"
        self.root_dir = ROOT_DIR
        print(f"ROOT_DIR: {self.root_dir}")
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
        if not os.path.exists(watchlist_path):
            with open(watchlist_path, 'w') as f:
                f.write('[]')
            print(f"Created empty watchlist at {watchlist_path}")
        self.watchdog = Watchdog(
            self.root_dir,
            os.path.join(self.root_dir, "ARTchain", "backups"),
            watchlist_path
        )
        self.weather_data = self.fetch_weather("Sint-Joris-Weert")
        print("ART init done.")

    def fetch_weather(self, location):
        if not self.api_keys["openweather"]:
            return "Weather: API key missing"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_keys['openweather']}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["main"]
                return f"{location} {temp:.1f}°C - {condition}"
            url = f"http://api.openweathermap.org/data/2.5/weather?lat=50.80&lon=4.87&appid={self.api_keys['openweather']}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["main"]
                return f"Sint-Joris-Weert {temp:.1f}°C - {condition}"
            return f"Sint-Joris-Weert - Error: {data['message']}"
        except Exception as e:
            return f"Sint-Joris-Weert - Error: {str(e)}"

    def respond(self, command):
        print(f"{self.name} heard: '{command}'")
        if command.lower() == "watchdog backup":
            self.watchdog.backup()
            return "Watchdog backup completed"
        elif command.lower().startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.watchdog.add(file_path)
            return f"Added {file_path} to watchdog"
        elif command.lower() == "watchdog rollback":
            if messagebox.askyesno("Watchdog", "Ready to rollback. Are ye sure?"):
                self.watchdog.rollback()
                return "Watchdog rollback completed"
            else:
                print("Watchdog: Rollback aborted—ye didn’t say YES!")
                return "Watchdog rollback aborted"
        elif command.lower() == "weather":
            self.weather_data = self.fetch_weather("Sint-Joris-Weert")
            return self.weather_data
        else:
            return self.core.respond(command)

if __name__ == "__main__":
    print("Main block starting...")
    try:
        root = tk.Tk()
        print("Tk root created.")
        art = ART()
        print("ART instance created.")
        app = Interface(root, art)
        print("Interface created.")
        print(f"{art.name} is online. Watchdog ready.")
        root.mainloop()
    except Exception as e:
        print(f"Main crashed: {e}")
        traceback.print_exc()
        sys.exit(1)