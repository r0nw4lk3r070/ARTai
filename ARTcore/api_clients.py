# ARTcore/api_clients.py - API Clients - 2025-03-14
import requests
import json  # Added!
from threading import Thread
from queue import Queue

class APIClients:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.nano_gpt_url = "https://nano-gpt.com/api/talk-to-gpt"
        self.grok_url = "https://api.xai.com/v1/chat/completions"
        self.nano_balance_url = "https://nano-gpt.com/api/check-nano-balance"
        self.response_queue = Queue()
        self.mode = "nanogpt" if api_keys.get("nano_gpt") else "offline"
        self.balance = self.check_balance() if self.mode == "nanogpt" else "N/A"
        print(f"API clients initialized in {self.mode} mode")

    def respond(self, command):
        print(f"Responding in mode: {self.mode}")
        if "api:grok" in command.lower():
            self.mode = "grok"
            return "Switched to Grok mode"
        elif "api:nanogpt" in command.lower():
            self.mode = "nanogpt"
            return "Switched to NanoGPT mode"
        elif "api:offline" in command.lower():
            self.mode = "offline"
            return "Switched to offline mode"

        if self.mode == "nanogpt":
            if not self.api_keys.get("nano_gpt"):
                return "NanoGPT: No API key, cap’n—check .env!"
            Thread(target=self._query_nano_gpt, args=(command,)).start()
            try:
                return self.response_queue.get(timeout=10)
            except Exception:
                print("NanoGPT timed out")
                return "NanoGPT: Timed out—server’s dodgy, cap’n!"
        elif self.mode == "grok":
            if not self.api_keys.get("grok_api"):
                return "Grok: No API key, cap’n—check .env!"
            Thread(target=self._query_grok, args=(command,)).start()
            try:
                return self.response_queue.get(timeout=10)
            except Exception:
                print("Grok timed out")
                return "Grok: Timed out—server’s dodgy, cap’n!"
        else:
            return "Offline mode—no APIs active, cap’n!"

    def _query_nano_gpt(self, prompt):
        try:
            headers = {"x-api-key": self.api_keys["nano_gpt"], "Content-Type": "application/json"}
            data = {"prompt": prompt, "model": "chatgpt-4o-latest", "messages": []}
            print(f"Querying NanoGPT with: {prompt}")
            response = requests.post(self.nano_gpt_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            raw = response.text
            parts = raw.split('<NanoGPT>')
            text_response = parts[0].strip()
            nano_info = json.loads(parts[1].split('</NanoGPT>')[0])
            result = f"{text_response} (Cost: {nano_info['cost']} Nano)"
            print(f"NanoGPT response: {result}")
            self.response_queue.put(result)
        except Exception as e:
            print(f"NanoGPT query failed: {str(e)}")
            self.response_queue.put(f"NanoGPT: Failed—{str(e)}, cap’n!")

    def _query_grok(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['grok_api']}", "Content-Type": "application/json"}
            data = {"model": "grok", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
            print(f"Querying Grok with: {prompt}")
            response = requests.post(self.grok_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            print(f"Grok response: {result}")
            self.response_queue.put(result)
        except Exception as e:
            print(f"Grok query failed: {str(e)}")
            self.response_queue.put(f"Grok: Failed—{str(e)}, cap’n!")

    def fetch_weather(self, location):
        if not self.api_keys.get("openweather"):
            return "Weather: API key missing"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_keys['openweather']}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["main"]
                print(f"Weather fetched: {location} {temp:.1f}°C - {condition}")
                return f"{location} {temp:.1f}°C - {condition}"
            return f"Weather fetch failed: {data['message']}"
        except Exception as e:
            print(f"Weather error: {str(e)}")
            return f"Weather error: {str(e)}"

    def check_balance(self):
        if not self.api_keys.get("nano_gpt"):
            return "NanoGPT Balance: No API key, cap’n!"
        try:
            headers = {"x-api-key": self.api_keys["nano_gpt"], "Content-Type": "application/json"}
            print("Checking NanoGPT balance...")
            response = requests.post(self.nano_balance_url, headers=headers, timeout=5)
            response.raise_for_status()
            balance_info = response.json()
            result = f"Balance: {balance_info['balance']} Nano"
            print(f"NanoGPT balance: {result}")
            return result
        except Exception as e:
            print(f"Balance check failed: {str(e)}")
            return f"Balance check failed—{str(e)}, cap’n!"