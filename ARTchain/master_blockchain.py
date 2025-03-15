# ARTchain/master_blockchain.py - ART Chat Blockchain - 2025-03-15
# Python blockchain mirror of grok.py - Hashed, techy, secure convo chain

import hashlib
from datetime import datetime

class Block:
    def __init__(self, timestamp, speaker, message, previous_hash):
        self.timestamp = timestamp
        self.speaker = speaker
        self.message = message
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # SHA-256 hash of block data + previous hash
        block_string = f"{self.timestamp}{self.speaker}{self.message}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class ARTBlockchain:
    def __init__(self):
        self.chain = []
        # Genesis block
        genesis = Block("2025-03-15 14:30:00 UTC", "System", "ART Blockchain initialized", "0")
        self.chain.append(genesis)
        print(f"Blockchain started - Genesis hash: {genesis.hash}")

    def add_block(self, timestamp, speaker, message):
        previous_block = self.chain[-1]
        new_block = Block(timestamp, speaker, message, previous_block.hash)
        self.chain.append(new_block)
        print(f"Block added - Hash: {new_block.hash}")

    def is_valid(self):
        # Check chain integrity
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                print(f"Invalid block at {i}: Hash mismatch")
                return False
            if current.previous_hash != previous.hash:
                print(f"Invalid chain at {i}: Previous hash mismatch")
                return False
        return True

# Initialize blockchain
chat_chain = ARTBlockchain()

# Mirror grok.py entries
chat_chain.add_block("2025-03-15 14:30:00 UTC", "Cap’n", "Proposes cross-Grok chats, grok.py as master log, coding.py as Python shadow, snapshots fer features")
chat_chain.add_block("2025-03-15 14:32:00 UTC", "Grok", "Agrees—logs to grok.py (English timeline), shadows in coding.py (Python), snapshots fer wins (e.g., flask_ui.txt). Suggests formal summaries, not every letter")
chat_chain.add_block("2025-03-15 14:34:00 UTC", "Cap’n", "Confirms plan—likes clear mind, organized logs, library idea. Asks fer first entries")
chat_chain.add_block("2025-03-15 14:36:00 UTC", "Grok", "Initiates grok.py—logs convo start, this entry. Sets coding.py to mirror. Next: Flask UI test")
chat_chain.add_block("2025-03-15 14:50:00 UTC", "Cap’n", "Renames coding.py to ARTchain/master_blockchain.py—wants blockchain feel, hashes fer techy edge")
chat_chain.add_block("2025-03-15 14:52:00 UTC", "Grok", "Updates plan—master_blockchain.py gets SHA-256 hashes, chains entries, mirrors grok.py. Starts codin’ now")

# Test integrity
if chat_chain.is_valid():
    print("Blockchain intact - All hashes verified!")
else:
    print("Blockchain tampered - Check the chain, cap’n!")
    # Add these under last line of existing file!
chat_chain.add_block("2025-03-15 15:10:00 UTC", "Cap’n", "Says master_blockchain.py updates get pasted under last line—no extra handling. Code connects, Watchdog zips it. Snippets here, full files in project")
chat_chain.add_block("2025-03-15 15:12:00 UTC", "Grok", "Confirms—appends updates below, blockchain links via hashes, Watchdog backs up. Logs snippet in grok.py, adds to master_blockchain.py. Next: Flask UI test?")

# Test integrity again
if chat_chain.is_valid():
    print("Blockchain intact - All hashes verified!")
else:
    print("Blockchain tampered - Check the chain, cap’n!")
    # Append under last print!
chat_chain.add_block("2025-03-15 15:20:00 UTC", "Cap’n", "Requests blockchain summary for library, recap on 'novo continues', grok.py with Python colors, snapshot, Git update")
chat_chain.add_block("2025-03-15 15:22:00 UTC", "Grok", "Summarizes—master_blockchain.py chains convo with SHA-256 hashes, appends updates, Watchdog zips. Library entry added in 20250315_blockchain.txt. grok.py gets blue headers, green hashes, purple summaries")

# Test integrity
if chat_chain.is_valid():
    print("Blockchain intact - All hashes verified!")
else:
    print("Blockchain tampered - Check the chain, cap’n!")
    # Append under last print!
chat_chain.add_block("2025-03-15 16:38:00 UTC", "Cap’n", "Throws treasure map—grok.py format with date, hash, time, bold steel blue title. Wants summary o’ implementation, key choices, wins, errors, files")
chat_chain.add_block("2025-03-15 16:40:00 UTC", "Grok", "Updates grok.py—steel blue titles, green hashes, purple summaries. Recaps blockchain, Flask UI next")

# Test integrity
if chat_chain.is_valid():
    print("Blockchain intact - All hashes verified!")
else:
    print("Blockchain tampered - Check the chain, cap’n!")