import os

# Base directory
ROOT_DIR = r"C:\Users\r0nw4\ART"

# .env path
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# API settings
API_KEYS = {
    "lights": "LIGHTS_API_KEY",
    "trading": "TRADING_API_KEY",
    "nano_gpt": "NANOGPT_API_KEY",
    "grok_api": "XAI_API_KEY",
    "openweather": "OPENWEATHER_API_KEY"
}

NANOGPT_API = {
    "base_url": "https://nano-gpt.com/api",
    "talk_endpoint": "/talk-to-gpt",
    "balance_endpoint": "/check-nano-balance",
    "headers": lambda key: {
        "x-api-key": key,
        "Content-Type": "application/json"
    },
    "default_model": "chatgpt-4o-latest",
    "max_tokens": 150,
    "temperature": 0.7
}

GROK_API = {
    "base_url": "https://api.x.ai/v1",
    "completions_endpoint": "/completions",
    "headers": lambda key: {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
    "max_tokens": 150,
    "temperature": 0.7
}

# Paths
WATCHDOG = {
    "backup_dir": os.path.join(ROOT_DIR, "ARTchain", "backups"),
    "watchlist_file": os.path.join(ROOT_DIR, "ARTchain", "watchlist.json")
}

REPORTS_DIR = os.path.join(ROOT_DIR, "ARTreports")
DB_DIR = os.path.join(ROOT_DIR, "ART_DB")

# GUI settings
CHAT_FONT = ("Arial", 14)
THEME = {
    "bg": "#1A1A1A",
    "fg": "#FFFDD0",
    "edge": "#FFFDD0"
}