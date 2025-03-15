# main.py - ART Core with APIs, DB, and CLI/Loop - 2025-03-14
import os
import sys
import sqlite3
import PyPDF2
from datetime import datetime
from dotenv import load_dotenv
from ARTchain.watchdog import Watchdog
from ARTcore.api_clients import APIClients
from ARTcore.prompts import Prompts
from ART_DB.db import ARTDB

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
        self._load_files()
        self._startup_report()

    def _load_files(self):
        print(f"Loadin’ files into ART’s brain from {self.learn_dir}—hold fast, cap’n!")
        with sqlite3.connect(self.db.db_path) as conn:
            existing = set(row[0] for row in conn.execute("SELECT source FROM knowledge"))
        files = os.listdir(self.learn_dir)
        if not files:
            print("No files found in ARTschool/learn—class be empty, cap’n!")
        loaded_files = []
        for file in files:
            filepath = os.path.join(self.learn_dir, file)
            if not os.path.isfile(filepath):
                print(f"Skipped non-file: {file}")
                continue
            if file in existing:
                print(f"Already in DB: {file}")
                os.remove(filepath)
                print(f"Cleared from learn: {file}")
                continue
            if not (file.endswith(".txt") or file.endswith(".py") or file.endswith(".pdf")):
                print(f"Skipped file (wrong type): {file}")
                continue
            try:
                if file.endswith(".txt") or file.endswith(".py"):
                    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                        self.db.store_file(file, f.read())
                elif file.endswith(".pdf"):
                    with open(filepath, "rb") as f:
                        pdf = PyPDF2.PdfReader(f)
                        content = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
                        self.db.store_file(file, content)
                loaded_files.append(file)
                os.remove(filepath)
                print(f"Loaded and cleared from learn: {file}")
            except Exception as e:
                print(f"Failed to load {file}: {str(e)}")
        if loaded_files:
            print("Files loaded into ART’s brain:")
            for f in loaded_files:
                print(f" - {f}")
        else:
            print("No new files loaded—ART’s brain be unchanged!")

    def _startup_report(self):
        print("ART core initialized")
        db_size = self.db.get_db_size()
        api_mode = self.api.mode
        api_model = "chatgpt-4o-latest" if api_mode == "nanogpt" else "N/A"
        balance = self.api.check_balance()
        weather = self.api.fetch_weather("Sint-Joris-Weert")
        print("ART online—ARTschool in session!")
        print("Full Ship’s Log:")
        print(f" - API Mode: {api_mode} (Model: {api_model})")
        print(f" - Balance: {balance} Nano")
        print(f" - DB Size: {db_size:.5f} GB")
        print(f" - Weather: {weather}")
        print("Type yer orders, cap’n! ('exit' to quit)")

    def respond(self, command):
        prompt_response = self.prompts.handle(command)
        if prompt_response is not None:
            response = prompt_response
        else:
            response = self.api.respond(command)
        self.db.log_chat(f"Command: {command} | Response: {response}")
        self._log_learned(command, response)
        return response

    def _log_learned(self, command, response):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.learned_dir, f"learned_{timestamp}.txt")
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Command: {command}\nResponse: {response}\n")
            print(f"Logged learnin’ to {log_file}")
        except Exception as e:
            print(f"Failed to log learnin’ to {log_file}: {str(e)}")

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
            art._log_learned(command, response)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"Logged learnin’ to {os.path.join(art.learned_dir, f'learned_{timestamp}.txt')}")
            print(response)
        else:
            response = art.respond(command)
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
            else:
                print(response)