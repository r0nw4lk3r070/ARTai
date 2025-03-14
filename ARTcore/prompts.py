# ARTcore/prompts.py - Prompt Handling - 2025-03-14
class Prompts:
    def __init__(self, art_instance):
        self.art = art_instance
        print("Prompts initialized")

    def handle(self, command):
        cmd = command.lower()
        if cmd == "watchdog backup":
            return self.art.watchdog.backup()
        elif cmd.startswith("watchdog add "):
            file_path = command.split("watchdog add ")[1].strip()
            self.art.watchdog.add(file_path)
            return f"Added {file_path}"
        elif cmd == "watchdog rollback":
            return self.art.watchdog.rollback()
        elif cmd == "api:nanogpt":
            self.art.api.mode = "nanogpt"
            return "Switched to NanoGPT mode"
        elif cmd == "api:grok":
            self.art.api.mode = "grok"
            return "Switched to Grok mode"
        elif cmd == "api:offline":
            self.art.api.mode = "offline"
            return "Switched to offline mode"
        elif cmd == "balance":
            return self.art.api.check_balance()
        else:
            return None  # Pass to API