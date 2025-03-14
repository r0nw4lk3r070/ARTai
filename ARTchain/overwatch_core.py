import os
from .overwatch_logging import log_action, api_call

class Overwatch:
    def __init__(self, log_dir):
        self.log_file = os.path.join(log_dir, "activity.log.jsonl")
        os.makedirs(log_dir, exist_ok=True)
        print("Overwatch initialized. Tracking ART's online moves.")

    def log(self, action, details):
        return log_action(self, action, details)

    def call_api(self, endpoint, payload):
        return api_call(self, endpoint, payload)