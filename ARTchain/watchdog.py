# ARTchain/watchdog.py - Watchdog Logic - 2025-03-14
import os
import time
import json

class Watchdog:
    def __init__(self, art_instance):
        self.art = art_instance
        self.root_dir = art_instance.root_dir
        self.backup_dir = os.path.join(self.root_dir, "ARTchain", "backups")
        self.watchlist_path = os.path.join(self.root_dir, "ARTchain", "watchlist.json")
        os.makedirs(self.backup_dir, exist_ok=True)
        if not os.path.exists(self.watchlist_path):
            with open(self.watchlist_path, 'w') as f:
                json.dump([], f)
        print("Watchdog initialized")

    def backup(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
        print(f"Backing up to {backup_path}")  # Zip logic TBD
        return backup_path

    def add(self, file_path):
        with open(self.watchlist_path, 'r+') as f:
            watchlist = json.load(f)
            if file_path not in watchlist:
                watchlist.append(file_path)
                f.seek(0)
                json.dump(watchlist, f)
        print(f"Watchdog added {file_path}")

    def rollback(self):
        print("Rolling back from latest backup")  # Restore logic TBD
        return "Rollback done"