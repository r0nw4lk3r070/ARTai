# ART Core - Debug NanoGPT/Grok - 2025-03-14
import os
import time
import json
import requests
from threading import Thread
from queue import Queue

class ARTCore:
    def __init__(self, root_dir, config, api_keys):
        self.root_dir = root_dir
        self.config = config
        self.start_time = time.time()
        self.db_dir = os.path.join(root_dir, "ART_DB")
        self.mode = self.config.get("preferred_mode", "offline")
        self.api_keys = api_keys
        self.nano_gpt_url = "https://api.n60f4x.com/v1/chat/completions"
        self.grok_url = "https://api.xai.com/v1/grok"
        self.response_queue = Queue()
        print(f"ARTCore initialized with {self.mode} mode")

    def is_active(self):
        return True

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
            except Exception as e:
                return f"Timeout waiting for NanoGPT: {str(e)}"
        elif self.mode == "grok" and self.api_keys.get("grok_api"):
            Thread(target=self._query_grok, args=(command,)).start()
            try:
                return self.response_queue.get(timeout=10)
            except Exception as e:
                return f"Timeout waiting for Grok: {str(e)}"
        else:
            return "Offline mode or no API key set"

    def _query_nano_gpt(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['nano_gpt']}", "Content-Type": "application/json"}
            data = {
                "model": "nano-gpt",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            print(f"Querying NanoGPT with: {prompt}")
            response = requests.post(self.nano_gpt_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            print(f"NanoGPT response: {result}")
            self.response_queue.put(result)
        except Exception as e:
            print(f"NanoGPT query failed: {str(e)}")
            self.response_queue.put(f"NanoGPT Error: {str(e)}")

    def _query_grok(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['grok_api']}", "Content-Type": "application/json"}
            data = {
                "model": "grok",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            print(f"Querying Grok with: {prompt}")
            response = requests.post(self.grok_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            result = response.json()
            if "choices" not in result or not result["choices"]:
                raise ValueError("No valid response from Grok API")
            grok_response = result["choices"][0]["message"]["content"].strip()
            print(f"Grok response: {grok_response}")
            self.response_queue.put(grok_response)
        except Exception as e:
            print(f"Grok query failed: {str(e)}")
            self.response_queue.put(f"Grok Error: {str(e)}")

    def get_balance(self):
        if self.api_keys.get("nano_gpt"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['nano_gpt']}"}
                response = requests.get(f"{self.nano_gpt_url}/balance", headers=headers, timeout=5)
                response.raise_for_status()
                balance_data = response.json()
                print(f"Balance fetched: {balance_data}")
                return balance_data
            except Exception as e:
                print(f"Failed to get NanoGPT balance: {e}")
                return None
        return None

    def _get_dataset_count(self):
        count = 0
        for _, _, files in os.walk(self.db_dir):
            count += len(files)
        return count

    def _load_dataset(self):
        dataset = []
        for root, _, files in os.walk(self.db_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        dataset.append(f.read())
                except Exception:
                    continue
        return dataset