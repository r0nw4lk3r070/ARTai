# ARTcore/startup.py - Startup Report - 2025-03-15
def startup_report(art):
    print("ART core initialized")
    db_size = art.db.get_db_size()
    api_mode = art.api.mode
    api_model = "chatgpt-4o-latest" if api_mode == "nanogpt" else "N/A"
    balance = art.api.check_balance()
    weather = art.api.fetch_weather("Sint-Joris-Weert")
    print("ART online—ARTschool in session!")
    print("Full Ship’s Log:")
    print(f" - API Mode: {api_mode} (Model: {api_model})")
    print(f" - Balance: {balance} Nano")  # Fixed—single Nano!
    print(f" - DB Size: {db_size:.5f} GB")
    print(f" - Weather: {weather}")
    print("Type yer orders, cap’n! ('exit' to quit)")