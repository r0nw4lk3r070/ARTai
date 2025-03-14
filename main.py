# main.py - ART Core with APIs - 2025-03-14
import os
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog
from ARTcore.api_clients import APIClients

class ART:
    def __init__(self):
        self.root_dir = "C:/Users/r0nw4/ART"
        load_dotenv(os.path.join(self.root_dir, ".env"))
        self.api_keys = {
            "nano_gpt": os.getenv("NANO_GPT_API_KEY"),
            "grok_api": os.getenv("GROK_API_KEY"),
            "openweather": os.getenv("OPENWEATHER_API_KEY")
        }
        self.watchdog = Watchdog(self)
        self.api = APIClients(self.api_keys)
        print("ART core initialized")

    def respond(self, command):
        if command.lower() == "watchdog backup":
            return self.watchdog.backup()
        elif command.lower().startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.watchdog.add(file_path)
            return f"Added {file_path}"
        elif command.lower() == "weather":
            return self.api.fetch_weather("Sint-Joris-Weert")
        else:
            return self.api.respond(command)

if __name__ == "__main__":
    art = ART()
    print("ART online")
    print(art.respond("watchdog backup"))
    print(art.respond("watchdog add test.txt"))
    print(art.respond("weather"))
    print(art.respond("oi mate"))