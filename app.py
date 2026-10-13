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
                "injury_notes": "Sam Houston WR1 (Questionable - Hamstring) • Limits deep vertical options",
                "morale_notes": "High Volatility • Body language from coaching staff brushing late-game defensive lapse"
            },
            {
                "id": "game_2",
                "sport": "CFB",
                "matchup": "South Florida @ UTSA",
                "venue": "Alamodome",
                "time_label": "THU 7:30 PM • UPCOMING",
                "spread_line": "UTSA -4.5",
                "ou_line": "O/U 58.5",
                "trajectory": "1,140 Miles West • 2 Time Zone Shift Effect",
                "crowd_env": "Dome Enclosure Noise Multiplier • Favors Ground Cadence",
                "injury_notes": "USF Starting Right Tackle (OUT - Ankle) • Weakens front edge protection",
                "morale_notes": "Stable Core • Focused on heavy trench script to offset line injuries"
            },
            {
                "id": "game_3",
                "sport": "NHL",
                "matchup": "Montreal Canadiens @ Boston Bruins",
                "venue": "TD Garden • Arena Main Track",
                "time_label": "THU 7:00 PM • UPCOMING",
                "spread_line": "Bruins Moneyline",
                "ou_line": "O/U 6.0",
                "trajectory": "310 Miles South • Minimal Rest Restriction Impact",
                "crowd_env": "TD Garden High Intensity • Amplifies Early Period Whistles",
                "injury_notes": "Boston Clear • Montreal Defenceman (Day-to-Day - Upper Body)",
                "morale_notes": "Rivalry Peak Intensity"
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
            --sky-blue: #58a6ff;
            --light-pink: #ff8ebb;
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
        .section-header {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
            margin: 16px 0 8px 0;
        }
        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-glow);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .automated-sheet {
            border: 1px solid var(--neon-green);
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: bold;
            margin-bottom: 4px;
        }
        .card-subtitle {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 12px;
        }
        .data-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin-bottom: 6px;
        }
        .highlight {
            color: var(--alert-orange);
            font-weight: bold;
        }
        .neon-text {
            color: var(--neon-green);
            font-weight: bold;
        }
        .metric-item {
            font-size: 0.85rem;
            margin-top: 8px;
            color: var(--text-main);
            line-height: 1.4;
        }
        .blue-text {
            color: var(--sky-blue);
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header-box">
            <div class="title-main">🟢 CEE SUPREME ACTION MATRIX</div>
            <div class="status-sync">LIVE SYNCING</div>
        </div>

        <!-- ⚡ AUTOMATED COMM SHEET SECTION -->
        <div class="section-header">⚡ LIVE AUTOMATED COMM SHEET</div>
        <div class="card automated-sheet">
            <div class="data-row">
                <span style="font-weight:bold; color:var(--sky-blue);">自由 LIVE SPREAD RECON</span>
                <span class="neon-text">👉 TAKE: Sam Houston Alternate Pass Yards (MORE 175.0 Floor)</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:8px;">Current market context target: Williams Stadium • Line: Liberty -13.5 (O/U 52.5).</div>
            
            <div class="data-row" style="margin-top:12px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <span style="font-weight:bold; color:var(--sky-blue);">自由 LIVE OVER/UNDER RECON</span>
                <span class="neon-text">👉 Analyzing Pacing</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:0;">Will display exact live points threshold targets based on quarter pacing.</div>
        </div>

        <!-- 👁️ SYNDICATE CONSENSUS SECTION -->
        <div class="section-header">👁️ SYNDICATE CONSENSUS & SENTIMENT VOLATILITY</div>
        <div class="card">
            <div class="data-row">
                <div>
                    <div style="font-weight:bold;">Alpha Syndicate</div>
                    <div style="font-size:0.75rem; color:var(--text-dim);">Size: 5x</div>
                </div>
                <div style="text-align:right;">
                    <div class="blue-text" style="font-weight:bold;">Sam Houston Pass Volume Sliders</div>
                    <div style="font-size:0.75rem; color:var(--alert-orange);">94% Public Resistance</div>
                </div>
            </div>
            <div class="data-row" style="margin-top:8px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <div>
                    <div style="font-weight:bold;">Vegas Sharp Box</div>
                    <div style="font-size:0.75rem; color:var(--text-dim);">Size: 2.5x</div>
                </div>
                <div style="text-align:right;">
                    <div class="blue-text" style="font-weight:bold;">NHL Under Adjustments</div>
                    <div style="font-size:0.75rem; color:var(--alert-orange);">74% Public Resistance</div>
                </div>
            </div>
        </div>

        <!-- 📺 LIVE SLATE & ADVANTAGE INSIGHTS SECTION -->
        <div class="section-header">📺 LIVE SLATE & HUMAN ADVANTAGE INSIGHTS</div>
        {% if feeds %}
            {% for game in feeds %}
            <div class="card">
