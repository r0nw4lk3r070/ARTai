import json
from datetime import datetime
import hashlib
import os

class Overwatch:
    def __init__(self, log_dir):
        self.log_file = os.path.join(log_dir, "activity.log.jsonl")
        os.makedirs(log_dir, exist_ok=True)

    def log_action(self, action, details):
        """Log an action with a hash."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "hash": hashlib.sha256(f"{action}{details}".encode()).hexdigest()
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def api_call(self, endpoint, payload):
        """Wrap API calls with logging (simulated for now)."""
        details = {"endpoint": endpoint, "payload": payload, "response": "simulated"}
        entry = self.log_action("API_CALL", details)
        print(f"Overwatch logged API call: {entry['hash'][:8]}...")
        return details["response"]