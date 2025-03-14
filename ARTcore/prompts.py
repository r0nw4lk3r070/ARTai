# ARTcore/prompts.py - Prompt Handling - 2025-03-14
class Prompts:
    def __init__(self, art_instance):
        self.art = art_instance
        print("Prompts initialized")

    def handle(self, command):
        if command.lower() == "watchdog backup":
            return self.art.watchdog.backup()
        elif command.lower().startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.art.watchdog.add(file_path)
            return f"Added {file_path}"
        elif command.lower() == "watchdog rollback":
            return self.art.watchdog.rollback()
        else:
            return None  # Pass to other handlers