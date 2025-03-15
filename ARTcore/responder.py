# ARTcore/responder.py - Response and Logging Logic - 2025-03-15
import os
from datetime import datetime

def respond(art, command, response=None):
    if response is None:
        prompt_response = art.prompts.handle(command)
        if prompt_response is not None:
            response = prompt_response
        else:
            response = art.api.respond(command)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(art.learned_dir, f"learned_{timestamp}.txt")
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Command: {command}\nResponse: {response}\n")
    except Exception as e:
        print(f"Failed to log learnin’ to {log_file}: {str(e)}")
    return response