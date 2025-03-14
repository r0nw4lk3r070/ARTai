import json
import datetime

def api_call(overwatch, api_name, details):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "api_name": api_name,
        "details": details
    }
    with open(overwatch.log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Overwatch logged API_CALL: {entry['api_name']} - {entry['details'][:20]}...")