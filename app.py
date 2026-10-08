import os
import json
import time
import datetime
import requests
from flask import Flask, render_template, jsonify, request, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

# 🐋 NEW ADDITION: CEE Syndicate Implied Probability Value Algorithm
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
            border-radius: 3px;
            font-weight: bold;
        }
        .banner-alert {
            background: linear-gradient(90deg, #3a221d, #161b22);
            border-left: 4px solid var(--alert-orange);
            padding: 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-bottom: 16px;
        }
        .recon-section {
            border: 1px dashed var(--neon-green);
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 16px;
            font-size: 0.85rem;
        }
        .section-label {
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
            display: block;
        }
        .whale-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-glow);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 14px;
        }
        .whale-card.active-alert {
            border-color: var(--alert-orange);
            box-shadow: 0 0 8px rgba(255, 159, 28, 0.2);
        }
        .whale-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: bold;
            font-size: 0.85rem;
            margin-bottom: 10px;
        }
        .whale-badge {
            font-size: 1.2rem;
            animation: pulse 2s infinite alternate;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.15); }
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            text-align: center;
            background: #0d1117;
            padding: 8px;
            border-radius: 4px;
        }
        .grid-val {
            font-size: 0.95rem;
            font-weight: bold;
            margin-top: 2px;
        }
        .text-high { color: var(--neon-green); }
        .text-alert { color: var(--alert-orange); }
        
        .footer-inputs {
            background-color: var(--bg-card);
            padding: 12px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            border-top: 1px solid var(--border-glow);
        }
        .unit-input-box {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .unit-input-box input {
            width: 45px;
            background: #0d1117;
            border: 1px solid var(--border-glow);
            color: #fff;
            padding: 6px;
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
        }
        .btn-update {
            background-color: var(--neon-green);
            color: #000;
            border: none;
            padding: 7px 14px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <form method="POST" action="/api/update_unit_form">
            <div class="header-box">
                <div class="title-main">🟢 CEE SUPREME ACTION MATRIX</div>
                <div class="status-sync">LIVE SYNCING</div>
            </div>

            <div class="banner-alert">
                ⚡ <strong>LIVE AUTOMATED COMM SHEET:</strong> SCANNING FEEDS
            </div>

            <div class="recon-section">
                <span class="section-label">📌 Target Strategy Play</span>
                <span style="color: var(--neon-green); font-weight: bold;">
                    TAKE: Sam Houston Alternate Pass Yards (MORE 175.0 Floor)
                </span>
            </div>

            <span class="section-label">👥 Syndicate Consensus & Sentiment Volatility</span>
            
            {% for game in games %}
                {% set gap = game.handle_pct - game.ticket_pct %}
                <div class="whale-card {% if gap >= 20 %}active-alert{% endif %}">
                    <div class="whale-header">
                        {% if gap >= 20 %}
                            <span class="whale-badge">🐋</span>
                            <span style="color: var(--alert-orange);">ALPHA SYNDICATE WHALE PLACEMENT</span>
                        {% else %}
                            <span>📊 STANDARD MARKET SPREAD</span>
                        {% endif %}
                    </div>
                    
                    <div style="font-size: 0.8rem; margin-bottom: 6px; color: var(--text-dim);">
                        <strong>{{ game.sport }}: {{ game.matchup }}</strong> | Spread: {{ game.spread_line }}
                    </div>

                    <div class="grid-3">
                        <div>
