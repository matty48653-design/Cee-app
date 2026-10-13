import os
import json
import time
import datetime
import requests
from flask import Flask, render_template, jsonify, request, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

# 🐋 CEE Syndicate Implied Probability Value Algorithm
def calculate_whale_probability_edge(american_odds, real_world_probability):
    if american_odds > 0:
        implied_prob = 100 / (american_odds + 100)
    else:
        implied_prob = abs(american_odds) / (abs(american_odds) + 100)
        
    edge_gap = real_world_probability - implied_prob
    
    if edge_gap >= 0.05:
        system_status = "🐋 ALPHA WHALE SIGNAL: HEAVY MISPRICING EXPOSED"
    elif edge_gap > 0:
        system_status = "📊 MARGINAL VALUE ATTAINED"
    else:
        system_status = "🪤 PUBLIC TRAP LINE: DEFENSIVE OVER-JUICING"
        
    return {
        "bookmaker_implied_prob_pct": round(implied_prob * 100, 2),
        "true_volume_probability_pct": round(real_world_probability * 100, 2),
        "extracted_edge_pct": round(edge_gap * 100, 2),
        "cee_matrix_signal": system_status
    }

# Core API Ingestion Function
def get_live_matrix_feeds():
    api_key = os.environ.get("SPORTS_DATA_KEY")
    
    # Fallback to local structured data if key isn't live
    if not api_key:
        return [
            {
                "id": "game_1",
                "sport": "CFB",
                "matchup": "Sam Houston @ Liberty",
                "venue": "Williams Stadium",
                "time_label": "THU 7:00 PM • UPCOMING",
                "spread_line": "Liberty -13.5",
                "ou_line": "O/U 52.5",
                "trajectory": "1,220 Miles East • Severe Fatigue Threshold Cross",
                "crowd_env": "Lynchburg Hostile • Decibel Index: High (Cap Playbook Comm)",
                "injury_notes": "INJURY MATRIX: Sam Houston WR1 (Questionable)",
                "rec_play": "Sam Houston Alternate Pass Yards (MORE 175.0 Floor)",
                "ticket_pct": 6,   
                "handle_pct": 44,  
            },
            {
                "id": "game_2",
                "sport": "NFL",
                "matchup": "Tampa Bay @ Dallas",
                "venue": "AT&T Stadium",
                "time_label": "THU 8:15 PM • UPCOMING",
                "spread_line": "Cowboys -8.5",
                "ou_line": "O/U 47.5",
                "trajectory": "Inside Territory • High Humidity Transition Floor",
                "crowd_env": "Arlington Loud • Structural Acoustics Maximized",
                "injury_notes": "INJURY MATRIX: Baker Mayfield OUT (Thumb) • Jalon Daniels Starting",
                "rec_play": "Jalon Daniels MORE 15+ Alternate Completions",
                "ticket_pct": 19,  
                "handle_pct": 52,  
            }
        ]
    
    url = "https://api-sports.io"
    headers = {"x-apisports-key": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get("results", [])
    except Exception:
        return []

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
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# Integrated Web Interface Layout Template Structure
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
            --border-glow: #21262d;
            --neon-green: #00ffaa;
            --text-main: #c9d1d9;
            --text-dim: #8b949e;
            --alert-orange: #ff9f1c;
        }
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 12px;
            display: flex;
            justify-content: center;
        }
        .app-container {
            width: 100%;
            max-width: 480px;
        }
        .header-box {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-glow);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }
        .title-main {
            font-weight: 800;
            letter-spacing: 1px;
            font-size: 1.1rem;
        }
        .status-sync {
            color: var(--neon-green);
            font-size: 0.75rem;
            border: 1px solid var(--neon-green);
            padding: 2px 6px;
            border-radius: 4px;
        }
        .matrix-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-glow);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .game-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .meta-line {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 8px;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            margin-top: 6px;
            font-size: 0.85rem;
        }
        .highlight-play {
            color: var(--alert-orange);
            font-weight: 600;
            border-top: 1px dashed var(--border-glow);
            margin-top: 8px;
            padding-top: 8px;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header-box">
            <div class="title-main">CEE ACTION MATRIX</div>
            <div class="status-sync">● SYSTEM LIVE</div>
        </div>
        
        {% for game in games %}
        <div class="matrix-card">
            <div class="game-title">[{{ game.sport }}] {{ game.matchup }}</div>
            <div class="meta-line">{{ game.time_label }} | {{ game.venue }}</div>
            
            <div class="metric-row">
                <span>Spread: <strong>{{ game.spread_line }}</strong></span>
                <span>Total: <strong>{{ game.ou_line }}</strong></span>
            </div>
            
            <div class="metric-row" style="font-size:0.8rem; color:var(--text-dim);">
                <span>Tickets: {{ game.ticket_pct }}%</span>
                <span>Handle Money: {{ game.handle_pct }}%</span>
            </div>
            
            <div style="font-size:0.75rem; margin-top:8px; color:var(--text-dim);">
                <div>📍 {{ game.trajectory }}</div>
                <div>🔊 {{ game.crowd_env }}</div>
                <div style="color:#ff6b6b;">⚠️ {{ game.injury_notes }}</div>
            </div>
            
            <div class="highlight-play">
                🎯 RECOMMENDED RUN: {{ game.rec_play }}
            </div>
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
