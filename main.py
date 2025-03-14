# main.py - ART Core with APIs, Prompts, DB, and CLI/Loop - 2025-03-14
import os
import sys
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog
from ARTcore.api_clients import APIClients
from ARTcore.prompts import Prompts
from ART_DB.db import ARTDB

class ART:
    def __init__(self):
        self.root_dir = "C:/Users/r0nw4/ART"
        load_dotenv(os.path.join(self.root_dir, ".env"))
        self.api_keys = {
            "nano_gpt": os.getenv("NANO_GPT_API_KEY"),
            "grok_api": os.getenv("GROK_API_KEY"),
            "openweather": os.getenv("OPENWEATHER_API_KEY")
        }
        self.watchdog = Watchdog(self)
        self.api = APIClients(self.api_keys)
        self.prompts = Prompts(self)
        self.db = ARTDB(self.root_dir)
        print("ART core initialized")

    def respond(self, command):
        prompt_response = self.prompts.handle(command)
        if prompt_response is not None:
            response = prompt_response
        else:
            response = self.api.respond(command)
        
        self.db.log_chat(f"Command: {command} | Response: {response}")
        return response

if __name__ == "__main__":
    art = ART()
    print("ART online")
    db_size = art.db.get_db_size()
    api_mode = art.api.mode
    api_model = "chatgpt-4o-latest" if api_mode == "nanogpt" else "N/A"
    if len(sys.argv) > 1:
        # CLI mode
        command = " ".join(sys.argv[1:])
        if command.lower() == "weather":
            response = art.api.fetch_weather("Sint-Joris-Weert")
            art.db.log_chat(f"Command: {command} | Response: {response}")
            print(f"API: {api_mode} (Model: {api_model}) | DB Size: {db_size:.5f} GB")
            print(response)
        else:
            response = art.respond(command)
            print(f"API: {api_mode} (Model: {api_model}) | DB Size: {db_size:.5f} GB")
            print(response)
    else:
        # Interactive loop
        print(f"Type yer orders, cap’n! ('exit' to quit) | API: {api_mode} (Model: {api_model}) | DB Size: {db_size:.5f} GB")
        while True:
            command = input("ART> ")
            if command.lower() == "exit":
                print("ART shuttin’ down—fair winds, cap’n!")
                break
            response = art.respond(command)
            db_size = art.db.get_db_size()
            api_mode = art.api.mode
            api_model = "chatgpt-4o-latest" if api_mode == "nanogpt" else "N/A"
            print(f"API: {api_mode} (Model: {api_model}) | DB Size: {db_size:.5f} GB")
            print(response)