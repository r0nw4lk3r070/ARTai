import os
import re
import json
import datetime
from ARTcore.api_integration import LLMIntegration
from ARTcore.prompts import MODE_DESCRIPTIONS, MAIN_HELP, COMMAND_HELP, ERROR_MESSAGES
from ART_DB.db_structure import ARTDatabase

class ARTCore:
    def __init__(self, root_dir, config, api_keys):
        self.root_dir = root_dir
        self.config = config
        self.api_keys = api_keys
        self.log_dir = os.path.join(root_dir, "ARTchain", "logs")
        self.start_time = datetime.datetime.now().timestamp()
        
        self.llm_integration = LLMIntegration(api_keys)  # No overwatch
        self.database = ARTDatabase(root_dir)
        self.conversation_history = []
        self.mode = config.get("preferred_mode", "grok")
        if self.mode not in ["grok", "nanogpt", "offline"]:
            self.mode = "grok"
        print(f"ARTCore initialized with {self.mode} mode")
    
    def is_active(self):
        return bool(self.api_keys.get("grok_api") or self.api_keys.get("nano_gpt") or self.config)

    def respond(self, command):
        self.conversation_history.append({"role": "user", "content": command})
        if command.upper().startswith("ART:"):
            response = self._handle_art_command(command[4:].strip())
        elif command.lower() == "help":
            response = MAIN_HELP
        elif command.lower().startswith("help "):
            topic = command.lower().split("help ")[1].strip()
            response = COMMAND_HELP.get(topic, f"No help available for '{topic}'")
        elif command.lower().startswith("api:"):
            response = self._switch_mode(command.lower().split("api:")[1].strip())
        elif command.lower() == "status":
            response = self._get_status()
        elif command.lower() == "go to school":
            response = self.go_to_school()
        else:
            response = self._process_query(command)
        self.conversation_history.append({"role": "assistant", "content": response})
        if len(self.conversation_history) > 20:
            self._save_conversation()
            self.conversation_history = self.conversation_history[-10:]
        return response
    
    def go_to_school(self):
        learn_path = os.path.join(self.root_dir, "ART_DB", "ARTschool", "learn")
        learned_path = os.path.join(self.root_dir, "ART_DB", "ARTschool", "learned")
        os.makedirs(learned_path, exist_ok=True)
        
        if not os.path.exists(learn_path):
            return "Learn folder not found!"
        
        results = []
        for filename in os.listdir(learn_path):
            file_path = os.path.join(learn_path, filename)
            content = ""
            if filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            elif filename.endswith(".pdf"):
                import PyPDF2
                with open(file_path, "rb") as f:
                    pdf = PyPDF2.PdfReader(f)
                    content = " ".join(page.extract_text() for page in pdf.pages)
            elif filename.endswith(".py"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                continue
            
            summary_prompt = f"Summarize this fully—juice, mood, story:\n{content}"
            summary = (self.llm_integration.query_grok(summary_prompt) if self.mode == "grok" else
                      self.llm_integration.query_nanogpt(summary_prompt) if self.mode == "nanogpt" else
                      {"choices": [{"text": "Offline: " + content[:100] + "..."}]})
            summary_text = summary.get("choices", [{}])[0].get("text", "Summary failed")
            
            self.database.add_dataset("learned_files", {"filename": filename, "content": content})
            json_data = {"filename": filename, "summary": summary_text, "mood": "neutral", "learned_at": datetime.datetime.now().isoformat()}
            with open(os.path.join(learned_path, f"{filename}.json"), "w") as f:
                json.dump(json_data, f, indent=2)
            os.remove(file_path)
            results.append(f"Learned {filename}")
        
        return "\n".join(results) or "No files to learn!"

    def _handle_art_command(self, query):
        print("ART command detected - processing cross-API")
        target_api = "grok" if self.mode == "nanogpt" else "nanogpt"
        if target_api not in self.llm_integration.available_models:
            return f"{target_api.capitalize()} not available!"
        
        lab_path = os.path.join(self.root_dir, "ARTlab")
        os.makedirs(lab_path, exist_ok=True)
        code_file = os.path.join(lab_path, "email_module.py")
        
        convo = [{"role": "user", "content": query}]
        response_text = ""
        for _ in range(5):
            prompt = f"Current code:\n{open(code_file, 'r').read() if os.path.exists(code_file) else 'None'}\n\n{query}\nLast response: {response_text}"
            if target_api == "grok":
                response = self.llm_integration.query_grok(prompt)
                response_text = response.get("choices", [{}])[0].get("text", "Grok error")
            else:
                response = self.llm_integration.query_nanogpt(prompt)
                response_text = response.get("choices", [{}])[0].get("text", "NanoGPT error")
            
            convo.append({"role": target_api, "content": response_text})
            
            code_match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
            if code_match:
                with open(code_file, "w") as f:
                    f.write(code_match.group(1))
                try:
                    compile(open(code_file, "r").read(), code_file, "exec")
                    break
                except SyntaxError as e:
                    query = f"Debug this error: {str(e)}"

        self.database.add_dataset("art_convos", {"query": query, "convo": convo})
        self.database.add_dataset("learned_files", {"filename": "email_module.py", "content": open(code_file, "r").read()})
        with open(os.path.join(self.root_dir, "ART_DB", "ARTschool", "learned", "email_module.json"), "w") as f:
            json.dump({"filename": "email_module.py", "summary": response_text, "mood": "codey", "learned_at": datetime.datetime.now().isoformat()}, f, indent=2)
        
        return f"Built with {target_api}! Code in ARTLab, convo logged."

    def _switch_mode(self, new_mode):
        if new_mode not in ["grok", "nanogpt", "offline"]:
            return ERROR_MESSAGES["invalid_command"]
        if new_mode == "grok" and "grok" not in self.llm_integration.available_models:
            return ERROR_MESSAGES["api_unavailable"].format(api_name="Grok")
        if new_mode == "nanogpt" and "nanogpt" not in self.llm_integration.available_models:
            return ERROR_MESSAGES["api_unavailable"].format(api_name="NanoGPT")
        self.mode = new_mode
        self.config["preferred_mode"] = new_mode
        return MODE_DESCRIPTIONS[new_mode]

    def _get_status(self):
        apis_available = self.llm_integration.available_models
        status = f"""
        ART SYSTEM STATUS
        =================
        Current Mode: {self.mode.upper()}
        
        APIs Available:
        - NanoGPT: {"✓" if "nanogpt" in apis_available else "✗"}
        - Grok: {"✓" if "grok" in apis_available else "✗"}
        
        Database:
        - Datasets: {self._get_dataset_count()}
        """
        return status

    def _get_dataset_count(self):
        try:
            index_path = os.path.join(self.database.datasets_path, "dataset_index.json")
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    index = json.load(f)
                return len(index.get("entries", []))
            return 0
        except:
            return 0

    def _process_query(self, query):
        if self.mode == "offline":
            return self._generate_offline_response(query)
        elif self.mode == "grok":
            response = self.llm_integration.query_grok(query)
            if "error" in response:
                return f"Error accessing Grok API: {response['error']}\nFalling back to offline mode."
            return response.get("choices", [{}])[0].get("text", "No response received")
        elif self.mode == "nanogpt":
            response = self.llm_integration.query_nanogpt(query)
            if "error" in response:
                return f"Error accessing NanoGPT API: {response['error']}\nFalling back to offline mode."
            return response.get("choices", [{}])[0].get("text", "No response received")
    
    def _generate_offline_response(self, query):
        try:
            dataset_path = os.path.join(self.database.datasets_path, "basic_qa", "data.json")
            if os.path.exists(dataset_path):
                with open(dataset_path, 'r') as f:
                    qa_data = json.load(f)
                for qa_pair in qa_data:
                    if query.lower() in qa_pair["question"].lower():
                        return qa_pair["answer"]
                return f"No offline data for that. Try 'api:grok' or 'api:nanogpt'."
            return "Offline database empty—run initial_data_loader.py."
        except Exception as e:
            return f"Offline error: {str(e)}"

    def _save_conversation(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        history_dir = os.path.join(self.database.conversation_history_path)
        os.makedirs(history_dir, exist_ok=True)
        filepath = os.path.join(history_dir, f"conversation_{timestamp}.json")
        with open(filepath, 'w') as f:
            json.dump({"timestamp": timestamp, "messages": self.conversation_history}, f, indent=2)