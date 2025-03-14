# ART Core - API Out - 2025-03-14
import os
import time

class ARTCore:
    def __init__(self, root_dir, api_settings):
        self.root_dir = root_dir
        self.start_time = time.time()
        self.db_dir = os.path.join(root_dir, "ART_DB")
        self.api = api_settings
        print("ARTCore initialized")

    def is_active(self):
        return True