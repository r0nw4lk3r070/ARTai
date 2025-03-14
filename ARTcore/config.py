class Config:
    # Grok API settings
    GROK_API_URL = "https://api.xai.com/v1/grok"
    GROK_HEADERS = {"Authorization": "Bearer YOUR_XAI_API_KEY", "Content-Type": "application/json"}
    GROK_MODEL = "grok-3"
    GROK_MAX_TOKENS = 4096
    GROK_COST_PER_M_INPUT = 0.000005
    GROK_COST_PER_M_OUTPUT = 0.000015

    # Nano GPT settings
    NANO_GPT_API_BASE_URL = "https://nano-gpt.com"
    NANO_GPT_API_BALANCE = f"{NANO_GPT_API_BASE_URL}/balance"
    NANO_GPT_HEADERS = {"Authorization": "Bearer YOUR_NANO_GPT_KEY", "Content-Type": "application/json"}
    NANO_GPT_MODEL = "chatgpt-4o-latest"

def load_config():
    config = {
        "lights_endpoint": "https://api.lights.example.com/control",
        "trading_endpoint": "https://api.trading.example.com/trade",
        "default_api": "nano_gpt",
        "grok_api": {
            "url": Config.GROK_API_URL,
            "headers": Config.GROK_HEADERS,
            "model": Config.GROK_MODEL,
            "max_tokens": Config.GROK_MAX_TOKENS,
            "cost_input": Config.GROK_COST_PER_M_INPUT,
            "cost_output": Config.GROK_COST_PER_M_OUTPUT
        },
        "nano_gpt": {
            "url": Config.NANO_GPT_API_BASE_URL,
            "balance_url": Config.NANO_GPT_API_BALANCE,
            "headers": Config.NANO_GPT_HEADERS,
            "model": Config.NANO_GPT_MODEL
        }
    }
    return config