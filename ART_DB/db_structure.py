import os
import json
import pickle
from datetime import datetime

class ARTDatabase:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.db_path = os.path.join(root_dir, "ART_DB")
        self.datasets_path = os.path.join(self.db_path, "datasets")
        self.embeddings_path = os.path.join(self.db_path, "embeddings")
        self.knowledge_path = os.path.join(self.db_path, "knowledge")
        self.conversation_history_path = os.path.join(self.db_path, "conversation_history")
        
        # Create directory structure if it doesn't exist
        for path in [self.db_path, self.datasets_path, self.embeddings_path, 
                    self.knowledge_path, self.conversation_history_path]:
            os.makedirs(path, exist_ok=True)
        
        # Create index files if they don't exist
        self._create_index_file(self.datasets_path, "dataset_index.json")
        self._create_index_file(self.embeddings_path, "embedding_index.json")
        self._create_index_file(self.knowledge_path, "knowledge_index.json")
    
    def _create_index_file(self, directory, filename):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump({"last_updated": datetime.now().isoformat(), "entries": []}, f, indent=2)
            print(f"Created index file: {filepath}")
    
    def add_dataset(self, name, description, data, format_type="text"):
        """Add a dataset to the database"""
        dataset_dir = os.path.join(self.datasets_path, name)
        os.makedirs(dataset_dir, exist_ok=True)
        
        # Save metadata
        metadata = {
            "name": name,
            "description": description,
            "created": datetime.now().isoformat(),
            "format": format_type,
            "size": len(data) if isinstance(data, list) else len(str(data)),
        }
        
        with open(os.path.join(dataset_dir, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save data based on format
        if format_type == "text":
            if isinstance(data, list):
                with open(os.path.join(dataset_dir, "data.txt"), 'w', encoding='utf-8') as f:
                    for item in data:
                        f.write(f"{item}\n")
            else:
                with open(os.path.join(dataset_dir, "data.txt"), 'w', encoding='utf-8') as f:
                    f.write(data)
        elif format_type == "json":
            with open(os.path.join(dataset_dir, "data.json"), 'w') as f:
                json.dump(data, f, indent=2)
        elif format_type == "pickle":
            with open(os.path.join(dataset_dir, "data.pkl"), 'wb') as f:
                pickle.dump(data, f)
        
        # Update index
        self._update_index(self.datasets_path, "dataset_index.json", name, metadata)
        
        return True
    
    def _update_index(self, directory, index_file, entry_name, metadata):
        filepath = os.path.join(directory, index_file)
        with open(filepath, 'r') as f:
            index = json.load(f)
        
        # Remove existing entry if present
        index["entries"] = [e for e in index["entries"] if e["name"] != entry_name]
        
        # Add new entry
        index["entries"].append({
            "name": entry_name,
            "added": datetime.now().isoformat(),
            "metadata": metadata
        })
        
        index["last_updated"] = datetime.now().isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(index, f, indent=2)