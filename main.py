# main.py - ART Core - 2025-03-14
import os
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog

class ART:
    def __init__(self):
        self.root_dir = "C:/Users/r0nw4/ART"
        load_dotenv(os.path.join(self.root_dir, ".env"))
        self.watchdog = Watchdog(self)
        print("ART core initialized")

    def respond(self, command):
        if command.lower() == "watchdog backup":
            return self.watchdog.backup()
        elif command.lower().startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.watchdog.add(file_path)
            return f"Added {file_path}"
        return "Command not recognized"

if __name__ == "__main__":
    art = ART()
    print("ART online")
    # Test commands
    print(art.respond("watchdog backup"))
    print(art.respond("watchdog add test.txt"))