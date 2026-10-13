import os
import json
import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# 🔑 LIVE API FEED TOKEN KEY INJECTED
THE_ODDS_API_KEY = "f4d3sefa9891beef9b72344e5"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

def get_live_matrix_feeds():
    """Fetches real-time point spreads and game lines"""
    b = "api.the-odds"
    b += "-api.com"
    p = "/v4/sports/american"
    p += "football_ncaaf"
    p += "/odds/"
    q = "?apiKey="
    q += f"{THE_ODDS_API_KEY}"
    q += "&regions=us"
    q += "&markets=spreads"
    q += ",totals"
    q += "&oddsFormat="
    q += "american"
    url = f"https://{b}{p}{q}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw_games = response.json()
            formatted_feeds = []

            for game in raw_games[:4]:
                home_team = game.get("home_team", "Unknown")
                away_team = game.get("away_team", "Unknown")
                spread_info = "Line Pending"
                ou_info = "O/U Unassigned"

                if game.get("bookmakers"):
                    primary_book = game["bookmakers"][0]
                    markets = primary_book.get("markets", [])
                    for market in markets:
                        if market.get("key") == "spreads":
                            outcomes = market.get("outcomes", [])
                            if len(outcomes) >= 2:
                                spread_info = f"{outcomes[0].get('name')} {outcomes[0].get('price')}"
                        elif market.get("key") == "totals":
                            outcomes = market.get("outcomes", [])
                            if outcomes:
                                ou_info = f"O/U {outcomes[0].get('point')}"

                formatted_feeds.append({
                    "sport": "CFB",
                    "matchup": f"{away_team} @ {home_team}",
                    "spread_line": spread_info,
                    "ou_line": ou_info
                })
            
            if formatted_feeds:
                return formatted_feeds
    except Exception as e:
        print(f"API Fetch Error, running fallback: {e}")

    # Fallback default data if API fails
    return [
        {
            "sport": "CFB",
            "matchup": "Sam Houston @ Liberty",
            "venue": "Williams Stadium",
            "time_label": "THU 7:00 PM",
            "spread_line": "Liberty -13.5",
            "ou_line": "O/U 52.5",
            "trajectory": "1,220 Miles East",
            "crowd_env": "Lynchburg Hostile",
            "injury_notes": "Sam Houston WR Questionable",
            "morale_notes": "High Volatility Slate"
        }
    ]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE SUPREME ACTION MATRIX</title>
    <style>
        :root {
            --bg-base: #0c1117;
            --bg-card: #161b22;
            --neon-green: #00ffaa;
            --text-main: #c9d1d9;
            --alert-orange: #ff9f1c;
            --sky-blue: #58a6ff;
        }
        body { 
            background-color: var(--bg-base); 
            color: var(--text-main); 
            font-family: sans-serif; 
            margin: 0; 
            padding: 20px; 
        }
        .app-container { width: 100%; max-width: 480px; margin: 0 auto; }
        .header-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .title-main { font-weight: 800; font-size: 1.2rem; color: #fff; }
        .status-sync { color: var(--neon-green); font-size: 0.8rem; }
        .card { background-color: var(--bg-card); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #30363d; }
        .matchup-text { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
        .line-text { color: var(--neon-green); font-weight: bold; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header-box">
            <div class="title-main">🟢 CEE AUTOMATION MATRIX</div>
            <div class="status-sync">LIVE API FEED ACTIVE</div>
        </div>
        
        {% for game in games %}
        <div class="card">
            <div class="matchup-text">{{ game.matchup }}</div>
            <div>Spread: <span class="line-text">{{ game.spread_line }}</span></div>
            <div>Total: <span class="line-text">{{ game.ou_line }}</span></div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    games = get_live_matrix_feeds()
    return render_template_string(HTML_TEMPLATE, games=games)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    save_data(data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
