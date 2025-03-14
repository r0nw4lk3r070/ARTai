import os
from dotenv import load_dotenv
from ARTcore.config import load_config
from ARTcore.art_core import ARTCore
from ARTchain.watchdog_core import Watchdog
from ARTchain.overwatch_core import Overwatch

class ART:
    def __init__(self):
        self.name = "ART"
        self.root_dir = r"C:\Users\r0nw4\ART"
        load_dotenv()
        self.api_keys = {
            "lights": os.getenv("LIGHTS_API_KEY"),
            "trading": os.getenv("TRADING_API_KEY"),
            "nano_gpt": os.getenv("NANO_GPT_API_KEY"),
            "grok_api": os.getenv("GROK_API_KEY"),
        }
        self.config = load_config()
        self.core = ARTCore(self.root_dir, self.config, self.api_keys)
        self.watchdog = Watchdog(
            self.root_dir,
            os.path.join(self.root_dir, "ARTchain", "backups"),
            os.path.join(self.root_dir, "ARTchain", "watchlist.json")
        )
        self.overwatch = Overwatch(os.path.join(self.root_dir, "ARTchain", "logs"))
        print(f"{self.name} is online. Watchdog and Overwatch ready.")

    def respond(self, command):
        print(f"{self.name} heard: '{command}'")
        if command.lower() == "watchdog backup":
            self.watchdog.backup()
        elif command.lower().startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.watchdog.add(file_path)
        elif command.lower() == "watchdog rollback":
            print("Watchdog: Ready to rollback. Are ye sure? Type YES to proceed.")
            confirmation = input("> ").strip().upper()
            if confirmation == "YES":
                self.watchdog.rollback()
            else:
                print("Watchdog: Rollback aborted—ye didn’t say YES!")
        else:
            self.core.respond(command)

if __name__ == "__main__":
    art = ART()
    while True:
        user_input = input("Tell ART what to do: ")
        art.respond(user_input)