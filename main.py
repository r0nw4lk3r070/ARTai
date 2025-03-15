# main.py - ART Core Glue - 2025-03-15
import os
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog
from ARTcore.api_clients import APIClients
from ARTcore.startup import startup_report
from ARTcore.responder import respond
from ARTschool.file_loader import load_files
from ART_DB.db import ARTDB
from ARTcore.prompts import Prompts

class ART:
    def __init__(self):
        self.root_dir = "C:/Users/r0nw4/ART"
        self.learn_dir = os.path.join(self.root_dir, "ARTschool", "learn")
        self.learned_dir = os.path.join(self.root_dir, "ARTschool", "learned")
        load_dotenv(os.path.join(self.root_dir, ".env"))
        self.api_keys = {
            "nano_gpt": os.getenv("NANO_GPT_API_KEY"),
            "grok_api": os.getenv("GROK_API_KEY"),
            "openweather": os.getenv("OPENWEATHER_API_KEY")
        }
        self.watchdog = Watchdog(self)
        self.api = APIClients(self.api_keys)
        self.db = ARTDB(self.root_dir)
        self.prompts = Prompts(self)
        os.makedirs(self.learn_dir, exist_ok=True)
        os.makedirs(self.learned_dir, exist_ok=True)
        load_files(self)
        startup_report(self)

if __name__ == "__main__":
    art = ART()
    while True:
        command = input("ART> ")
        if command.lower() == "exit":
            print("ART shuttin’ down—fair winds, cap’n!")
            break
        elif command.lower() == "weather":
            response = art.api.fetch_weather("Sint-Joris-Weert")
            art.db.log_chat(f"Command: {command} | Response: {response}")
            respond(art, command, response=response)
            print(response)
        else:
            response = respond(art, command)
            api_mode = art.api.mode
            balance = art.api.check_balance()
            if api_mode == "nanogpt" and "Cost" in response:
                cost_start = response.find("(Cost: ")
                if cost_start != -1:
                    cost_end = response.find(" Nano)") + 6
                    cost_str = response[cost_start + 7:cost_end - 6]
                    response_clean = response[:cost_start].strip()
                    print(f"{response_clean} (Cost: {cost_str} Nano, Balance: {balance} Nano)")
            else:
                print(response)