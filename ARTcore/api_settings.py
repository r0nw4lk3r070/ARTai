# API Settings - All-in-One - 2025-03-14
import os
import requests
from threading import Thread
from queue import Queue

class APISettings:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.nano_gpt_url = "https://api.n60f4x.com/v1/chat/completions"
        self.grok_url = "https://api.xai.com/v1/chat/completions"
        self.response_queue = Queue()
        self.last_balance = {"balance": 2.8782}  # Mock fer now
        self.mode = "nanogpt" if api_keys.get("nano_gpt") else "offline"

    def respond(self, command):
        print(f"Responding in mode: {self.mode}")
        if "api:grok" in command.lower():
            self.mode = "grok"
            return "Switched to Grok mode"
        elif "api:nanogpt" in command.lower():
            self.mode = "nanogpt"
            return "Switched to NanoGPT mode"

        if self.mode == "nanogpt" and self.api_keys.get("nano_gpt"):
            Thread(target=self._query_nano_gpt, args=(command,)).start()
            try:
                return self.response_queue.get(timeout=10)
            except Exception:
                print("NanoGPT timed out")
                return "NanoGPT offline: Server’s lost, cap’n!"
        elif self.mode == "grok" and self.api_keys.get("grok_api"):
            Thread(target=self._query_grok, args=(command,)).start()
            try:
                return self.response_queue.get(timeout=10)
            except Exception:
                print("Grok timed out")
                return "Grok offline: Auth failed—check yer key, mate!"
        else:
            return "Offline mode—no APIs ready, cap’n!"

    def _query_nano_gpt(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['nano_gpt']}", "Content-Type": "application/json"}
            data = {"model": "nano-gpt", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
            print(f"Querying NanoGPT with: {prompt}")
            response = requests.post(self.nano_gpt_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            print(f"NanoGPT response: {result}")
            self.response_queue.put(result)
        except Exception as e:
            print(f"NanoGPT query failed: {str(e)}")
            self.response_queue.put(f"NanoGPT offline: Server’s lost, cap’n!")

    def _query_grok(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['grok_api']}", "Content-Type": "application/json"}
            data = {"model": "grok", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
            print(f"Querying Grok with: {prompt}")
            response = requests.post(self.grok_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            result = response.json()
            print(f"Grok raw response: {result}")
            if "choices" not in result or not result["choices"]:
                raise ValueError("No valid response from Grok API")
            grok_response = result["choices"][0]["message"]["content"].strip()
            print(f"Grok response: {grok_response}")
            self.response_queue.put(grok_response)
        except Exception as e:
            print(f"Grok query failed: {str(e)}")
            self.response_queue.put(f"Grok offline: Auth failed—check yer key, mate!")

    def get_balance(self):
        if self.api_keys.get("nano_gpt"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['nano_gpt']}"}
                response = requests.get(f"{self.nano_gpt_url}/balance", headers=headers, timeout=5)
                response.raise_for_status()
                balance_data = response.json()
                print(f"Balance fetched: {balance_data}")
                self.last_balance = balance_data
                return balance_data
            except Exception as e:
                print(f"Failed to get NanoGPT balance: {e}")
                return self.last_balance if self.last_balance else {"balance": 0.0}
        return {"balance": 0.0}