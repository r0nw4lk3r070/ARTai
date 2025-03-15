# art_project.py
# ART: A local AI with X bot capabilities, NanoGPT/Grok API integration, and Flask UI
# Date: March 15, 2025
# Summary: CPU-only setup (no GPU yet), tweets via X API, uses APIs for now (no offline training)

"""
### Roadmap Overview
- Phase 1: Initial Setup - Environment, basic structure.
- Phase 2: API Integration - Grok (xAI) and NanoGPT (nano-gpt.com).
- Phase 3: Watchdog - Backup system with ZIP files (placeholder).
- Phase 4: Flask UI - Chat, content, stats cockpit.
- Phase 5: Offline Brain - Skipped for now (CPU-only, no training yet).
- Phase 6: X Bot - Tweet via X API with keyword-driven API responses.
- Notes: One-day base setup done; training is ongoing. Focus on APIs + X bot.
"""

import os
import requests
import tweepy
from flask import Flask, render_template, request
from dotenv import load_dotenv  # pip install python-dotenv

# Load API keys from .env
load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")
NANO_API_KEY = os.getenv("NANO_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# X API setup with Tweepy
auth = tweepy.OAuth1UserHandler(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
x_client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

# API functions
def call_grok(prompt):
    url = "https://api.xai.com/grok"  # Check xAI docs for exact endpoint
    headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": prompt, "model": "grok-2"}
    response = requests.post(url, json=data, headers=headers)
    return response.json().get("response", "Error")

def call_nanogpt(prompt, model="chatgpt-4o-latest"):
    url = "https://nano-gpt.com/api/v1/chat"
    headers = {"x-api-key": NANO_API_KEY, "Content-Type": "application/json"}
    data = {"prompt": prompt, "model": model}
    response = requests.post(url, json=data, headers=headers)
    return response.json()["reply"] if response.status_code == 200 else f"Error: {response.text}"

# Tweet function
def tweet_art(message):
    try:
        x_client.create_tweet(text=message[:280])  # 280 char limit
        print(f"Tweeted: {message}")
        return True
    except Exception as e:
        print(f"Error tweeting: {e}")
        return False

# Keyword-driven ART query
KEYWORDS = ["AI", "creativity", "tech"]  # Customize these
def query_art(prompt, api="grok", tweet=False):
    stats["query_count"] += 1
    full_prompt = f"Generate a short, witty tweet about {', '.join(KEYWORDS)}. Prompt: {prompt}"
    if api == "grok":
        response = call_grok(full_prompt)
    elif api == "nanogpt":
        response = call_nanogpt(full_prompt)
    else:
        response = "No API selected"
    if tweet and len(response) <= 280:
        tweet_art(response)
    return response

# Flask setup
app = Flask(__name__)
stats = {"query_count": 0}

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        api = request.form.get("api", "grok")
        tweet = "tweet" in request.form
        response = query_art(prompt, api, tweet)
    return render_template("index.html", response=response, stats=stats)

# Placeholder for future features (watchdog, offline brain)
def start_art():
    print("ART is running...")

if __name__ == "__main__":
    start_art()
    app.run(debug=True)

"""
### Setup Instructions
1. Create virtualenv: python3 -m venv art_env; source art_env/bin/activate
2. Install: pip install requests flask tweepy python-dotenv
3. Create .env with API keys:
   GROK_API_KEY=your_key
   NANO_API_KEY=your_key
   X_API_KEY=your_key
   X_API_SECRET=your_secret
   X_ACCESS_TOKEN=your_token
   X_ACCESS_TOKEN_SECRET=your_token_secret
4. Create templates/index.html (see below)
5. Run: python art_project.py
6. Visit: http://localhost:5000

### templates/index.html (save in templates/ folder)
<!DOCTYPE html>
<html>
<head><title>ART Interface</title></head>
<body>
    <h1>ART Interface</h1>
    <h2>Chat</h2>
    <form method="POST">
        <input type="text" name="prompt" placeholder="Ask ART...">
        <select name="api">
            <option value="grok">Grok</option>
            <option value="nanogpt">NanoGPT</option>
        </select>
        <input type="submit" value="Send">
        <input type="submit" name="tweet" value="Send & Tweet">
    </form>
    <p>{{ response }}</p>
    <h2>Content</h2>
    <p>Generated content: {{ response if response else "Enter a prompt above" }}</p>
    <h2>Stats Cockpit</h2>
    <p>Queries made: {{ stats.query_count }}</p>
</body>
</html>

### Notes
- X API: Free tier = 1,500 tweets/month (~50/day).
- Offline Brain: Skipped for now; add later with GPU.
- Figma UI: Design visually, adapt into index.html (in progress).
- Next Ideas: Dynamic keywords, scheduled tweets, stats for tweets sent.
"""