# ARTschool/file_loader.py - File Loading Logic - 2025-03-15
import os
import sqlite3
import PyPDF2

def load_files(art):
    print(f"Loadin’ files into ART’s brain from {art.learn_dir}—hold fast, cap’n!")
    with sqlite3.connect(art.db.db_path) as conn:
        existing = set(row[0] for row in conn.execute("SELECT source FROM knowledge"))
    files = os.listdir(art.learn_dir)
    if not files:
        print("No files found in ARTschool/learn—class be empty, cap’n!")
    loaded_files = []
    for file in files:
        filepath = os.path.join(art.learn_dir, file)
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
                    art.db.store_file(file, f.read())
            elif file.endswith(".pdf"):
                with open(filepath, "rb") as f:
                    pdf = PyPDF2.PdfReader(f)
                    content = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
                    art.db.store_file(file, content)
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