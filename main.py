# Main - Slim APIs + Watchdog + Weather - 2025-03-14
import os
import sys
import traceback
import tkinter as tk
from dotenv import load_dotenv
from tkinter import messagebox
import requests
from ARTcore.interface.interface import ARTInterface
from ARTcore.api_settings import APISettings
from ARTchain.watchdog import Watchdog

print("Starting imports...")
load_dotenv()
print("Imports done, defining ART...")

class ART:
    def __init__(self):
        print("ART init started...")
        self.name = "ART"
        self.root_dir = "C:/Users/r0nw4/ART"
        print(f"ROOT_DIR: {self.root_dir}")
        print(f"Loading .env from: {self.root_dir}/.env")
        self.api_keys = {
            "lights": os.getenv("LIGHTS_API_KEY"),
            "trading": os.getenv("TRADING_API_KEY"),
            "nano_gpt": os.getenv("NANO_GPT_API_KEY"),
            "grok_api": os.getenv("GROK_API_KEY"),
            "openweather": os.getenv("OPENWEATHER_API_KEY")
        }
        print("Loaded API keys:")
        for key, value in self.api_keys.items():
            print(f"{key}: {'Set' if value else 'Not set'}")
        
        self.api = APISettings(self.api_keys)
        self.watchdog = Watchdog(self)
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
            return self.api.respond(command)

if __name__ == "__main__":
    print("Main block starting...")
    try:
        root = tk.Tk()
        print("Tk root created.")
        art = ART()
        print("ART instance created.")
        app = ARTInterface(root, art)
        print("Interface created.")
        print(f"{art.name} is online. Watchdog ready.")
        root.mainloop()
    except Exception as e:
        print(f"Main crashed: {e}")
        traceback.print_exc()
        sys.exit(1)