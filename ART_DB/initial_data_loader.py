import os
from ART_DB.db_structure import ARTDatabase

def load_initial_datasets():
    """Load initial datasets into the ART database"""
    db = ARTDatabase(os.path.dirname(os.path.dirname(__file__)))
    
    # Example: Add a basic Q&A dataset
    qa_data = [
        {"question": "What is your name?", "answer": "My name is ART, the Autonomous Runtime Tool."},
        {"question": "Who created you?", "answer": "I was created by my developer to assist with various tasks and provide information."},
        {"question": "What can you do?", "answer": "I can help with answering questions, monitoring files, backing up important data, and connecting to various services."},
        {"question": "How do you work?", "answer": "I use a combination of local processing and, when available, API connections to language models like Grok and NanoGPT."}
    ]
    
    db.add_dataset(
        name="basic_qa",
        description="Basic questions and answers about ART",
        data=qa_data,
        format_type="json"
    )
    
    print("Initial datasets loaded into ART_DB")

if __name__ == "__main__":
    load_initial_datasets()