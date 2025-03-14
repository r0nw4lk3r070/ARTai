import os
import requests
import json

class LLMIntegration:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.available_models = self._check_available_models()
    
    def _check_available_models(self):
        models = []
        if self.api_keys.get("grok_api"):
            models.append("grok")
        if self.api_keys.get("nano_gpt"):
            models.append("nanogpt")
        return models
    
    def query_grok(self, prompt, max_tokens=150, temperature=0.7):
        if "grok" not in self.available_models:
            print("Grok: API key not available")
            return {"error": "Grok API key not configured"}
        try:
            headers = {"Authorization": f"Bearer {self.api_keys['grok_api']}", "Content-Type": "application/json"}
            payload = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
            response = requests.post("https://api.x.ai/v1/completions", headers=headers, json=payload)
            response_data = response.json()
            print(f"Grok: Queried - {json.dumps(payload)} -> {json.dumps(response_data)}")
            return response_data
        except Exception as e:
            print(f"Grok: Error querying - {str(e)}")
            return {"error": str(e)}
    
    def query_nanogpt(self, prompt, max_tokens=150, temperature=0.7):
        if "nanogpt" not in self.available_models:
            print("NanoGPT: API key not available")
            return {"error": "NanoGPT API key not configured"}
        try:
            headers = {
                "x-api-key": self.api_keys["nano_gpt"],  # Updated key name
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "model": "chatgpt-4o-latest",
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post("https://nano-gpt.com/api/talk-to-gpt", headers=headers, json=data)
            if response.status_code == 200:
                raw_response = response.text
                print(f"NanoGPT: Raw response - {raw_response}")
                parts = raw_response.split('<NanoGPT>')
                text_response = parts[0].strip()
                nano_info = json.loads(parts[1].split('</NanoGPT>')[0]) if len(parts) > 1 else {}
                return {"choices": [{"text": text_response}], "nano_info": nano_info}
            else:
                print(f"NanoGPT: Failed - Status {response.status_code}, {response.text}")
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            print(f"NanoGPT: Error querying - {str(e)}")
            return {"error": str(e)}
    
    def get_balance(self):
        if "nanogpt" not in self.available_models:
            print("NanoGPT: API key not available for balance check")
            return None
        try:
            headers = {
                "x-api-key": self.api_keys["nano_gpt"],  # Updated key name
                "Content-Type": "application/json"
            }
            response = requests.post("https://nano-gpt.com/api/check-nano-balance", headers=headers)
            response.raise_for_status()
            balance_info = response.json()
            print(f"NanoGPT Balance: {balance_info['balance']} Nano")
            return balance_info
        except requests.RequestException as e:
            print(f"NanoGPT: Error checking balance - {str(e)}")
            return None
    
    def get_best_response(self, prompt, prefer_model=None):
        if prefer_model and prefer_model in self.available_models:
            if prefer_model == "grok":
                return self.query_grok(prompt)
            elif prefer_model == "nanogpt":
                return self.query_nanogpt(prompt)
        if "grok" in self.available_models:
            return self.query_grok(prompt)
        elif "nanogpt" in self.available_models:
            return self.query_nanogpt(prompt)
        return {"error": "No LLM APIs configured"}