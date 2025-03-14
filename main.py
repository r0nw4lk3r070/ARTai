# main.py - ART Core with APIs, Prompts, and CLI/Loop - 2025-03-14
import os
import sys
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog
from ARTcore.api_clients import APIClients
from ARTcore.prompts import Prompts

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
        print("ART core initialized")

    def respond(self, command):
        prompt_response = self.prompts.handle(command)
        if prompt_response is not None:
            return prompt_response
        
        if command.lower() == "weather":
            return self.api.fetch_weather("Sint-Joris-Weert")
        else:
            return self.api.respond(command)

if __name__ == "__main__":
    art = ART()
    print("ART online")
    if len(sys.argv) > 1:
        # CLI mode
        command = " ".join(sys.argv[1:])
        print(art.respond(command))
    else:
        # Interactive loop
        print("Type yer orders, cap’n! ('exit' to quit)")
        while True:
            command = input("ART> ")
            if command.lower() == "exit":
                print("ART shuttin’ down—fair winds, cap’n!")
                break
            response = art.respond(command)
            print(response)