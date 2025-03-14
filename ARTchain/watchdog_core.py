import os
import json
import shutil
import datetime

class Watchdog:
    def __init__(self, root_dir, backup_dir, watchlist_file):
        self.root_dir = root_dir
        self.backup_dir = backup_dir
        self.watchlist_file = watchlist_file
        os.makedirs(backup_dir, exist_ok=True)
        if not os.path.exists(watchlist_file):
            with open(watchlist_file, "w") as f:
                json.dump([], f)

    def backup(self):
        """Backup files in watchlist"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_path, exist_ok=True)
        
        with open(self.watchlist_file, "r") as f:
            watchlist = json.load(f)
        
        for file_path in watchlist:
            if os.path.exists(file_path):
                rel_path = os.path.relpath(file_path, self.root_dir)
                dest_path = os.path.join(backup_path, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
                print(f"Backed up {file_path} to {dest_path}")
            else:
                print(f"File not found for backup: {file_path}")
        
        print(f"Backup completed to {backup_path}")

    def add(self, file_path):
        """Add a file to the watchlist"""
        with open(self.watchlist_file, "r") as f:
            watchlist = json.load(f)
        
        if file_path not in watchlist:
            watchlist.append(file_path)
            with open(self.watchlist_file, "w") as f:
                json.dump(watchlist, f, indent=2)
            print(f"Added {file_path} to watchlist")
        else:
            print(f"{file_path} already in watchlist")

    def rollback(self):
        """Rollback to latest backup"""
        backups = sorted([d for d in os.listdir(self.backup_dir) if d.startswith("backup_")], reverse=True)
        if not backups:
            print("No backups found!")
            return
        
        latest_backup = os.path.join(self.backup_dir, backups[0])
        with open(self.watchlist_file, "r") as f:
            watchlist = json.load(f)
        
        for file_path in watchlist:
            backup_file = os.path.join(latest_backup, os.path.relpath(file_path, self.root_dir))
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, file_path)
                print(f"Restored {file_path} from {backup_file}")
            else:
                print(f"No backup found for {file_path}")
        
        print(f"Rollback completed from {latest_backup}")