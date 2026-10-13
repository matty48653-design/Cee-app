import os
import json
import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

def get_live_matrix_feeds():
    return [
        {
            "sport": "CFB",
            "matchup": "Sam Houston @ Liberty",
            "venue": "Williams Stadium",
            "time_label": "THU 7:00 PM • UPCOMING",
            "spread_line": "Liberty -13.5",
            "ou_line": "O/U 52.5",
            "trajectory": "1,220 Miles East • Severe Fatigue Threshold Cross",
            "crowd_env": "Lynchburg Hostile • Decibel Index: High (Cap Playbook Comm)",
            "injury_notes": "Sam Houston WR1 (Questionable - Hamstring) • Limits deep vertical options",
            "morale_notes": "High Volatility • Coaching staff brushing late-game defensive lapse"
        },
        {
            "sport": "CFB",
            "matchup": "South Florida @ UTSA",
            "venue": "Alamodome",
            "time_label": "THU 7:30 PM • UPCOMING",
            "spread_line": "UTSA -4.5",
            "ou_line": "O/U 58.5",
            "trajectory": "1,140 Miles West • 2 Time Zone Shift Effect",
            "crowd_env": "Dome Enclosure Noise Multiplier • Favors Ground Cadence",
            "injury_notes": "USF Starting Right Tackle (OUT - Ankle) • Weakens front edge protection",
            "morale_notes": "Stable Core • Heavy trench script to offset line injuries"
        },
        {
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
            --bg-base: #0c1117; --bg-card: #161b22; --border-glow: #21262d;
            --neon-green: #00ffaa; --text-main: #c9d1d9; --text-dim: #8b949e;
            --alert-orange: #ff9f1c; --sky-blue: #58a6ff; --light-pink: #ff8ebb;
        }
        body { background-color: var(--bg-base); color: var(--text-main); font-family: sans-serif; margin: 0; padding: 12px; display: flex; justify-content: center; }
        .app-container { width: 100%; max-width: 480px; }
        .header-box { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border-glow); padding-bottom: 8px; margin-bottom: 16px; }
        .title-main { font-weight: 800; font-size: 1.1rem; }
        .status-sync { color: var(--neon-green); font-size: 0.75rem; border: 1px solid var(--neon-green); padding: 2px 6px; border-radius: 4px; }
        .section-header { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin: 16px 0 8px 0; }
        .card { background-color: var(--bg-card); border: 1px solid var(--border-glow); border-radius: 8px; padding: 14px; margin-bottom: 12px; }
        .automated-sheet { border: 1px solid var(--neon-green); }
        .card-title { font-size: 1.05rem; font-weight: bold; margin-bottom: 4px; }
        .card-subtitle { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 12px; }
        .data-row { display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px; }
        .highlight { color: var(--alert-orange); font-weight: bold; }
        .neon-text { color: var(--neon-green); font-weight: bold; }
        .metric-item { font-size: 0.85rem; margin-top: 8px; line-height: 1.4; }
        .blue-text { color: var(--sky-blue); }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header-box">
            <div class="title-main">🟢 CEE SUPREME ACTION MATRIX</div>
            <div class="status-sync">LIVE SYNCING</div>
        </div>

        <div class="section-header">⚡ LIVE AUTOMATED COMM SHEET</div>
        <div class="card automated-sheet">
            <div class="data-row">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE SPREAD RECON</span>
                <span class="neon-text">👉 TAKE: Sam Houston Alternate Pass Yards (MORE 175.0 Floor)</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:8px;">Current market context target: Williams Stadium • Line: Liberty -13.5 (O/U 52.5).</div>
            <div class="data-row" style="margin-top:12px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE OVER/UNDER RECON</span>
                <span class="neon-text">👉 Analyzing Pacing</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:0;">Will display exact live points threshold targets based on quarter pacing.</div>
        </div>

        <div class="section-header">👁️ SYNDICATE CONSENSUS & SENTIMENT VOLATILITY</div>
        <div class="card">
            <div class="data-row">
                <div><strong>Alpha Syndicate</strong><br><span style="font-size:0.75rem;color:var(--text-dim);">Size: 5x</span></div>
                <div style="text-align:right;"><span class="blue-text" style="font-weight:bold;">Sam Houston Pass Volume Sliders</span><br><span style="font-size:0.75rem;color:var(--alert-orange);">94% Public Resistance</span></div>
            </div>
            <div class="data-row" style="margin-top:8px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <div><strong>Vegas Sharp Box</strong><br><span style="font-size:0.75rem;color:var(--text-dim);">Size: 2.5x</span></div>
                <div style="text-align:right;"><span class="blue-text" style="font-weight:bold;">NHL Under Adjustments</span><br><span style="font-size:0.75rem;color:var(--alert-orange);">74% Public Resistance</span></div>
            </div>
        </div>

        <div class="section-header">📺 LIVE SLATE & HUMAN ADVANTAGE INSIGHTS</div>
        {% for game in feeds %}
        <div class="card">
            <div class="data-row">
                <span class="card-title">{{ game.sport }} {{ game.matchup }}</span>
                <span class="neon-text">0 - 0</span>
            </div>
            <div class="card-subtitle">{{ game.venue }} • Line: {{ game.spread_line }} ({{ game.ou_line }}) • <span class="highlight">{{ game.time_label }}</span></div>
            <div class="metric-item">🚀 <span class="blue-text" style="font-weight:bold;">TRAVEL TRAJECTORY:</span> {{ game.trajectory }}</div>
            <div class="metric-item">🔊 <span style="color:#ff4444; font-weight:bold;">CROWD ENVIRONMENT:</span> {{ game.crowd_env }}</div>
            <div class="metric-item">⚠️ <span class="highlight" style="font-weight:bold;">INJURY MATRIX:</span> {{ game.injury_notes }}</div>
            <div class="metric-item">🧠 <span style="color:var(--light-pink); font-weight:bold;">ROSTER MORALE:</span> {{ game.morale_notes }}</div>
        </div>
        {% endfor %}

        <div class="section-header">🐋 LIVE AUTOMATED WHALE MOVES</div>
        {% if whale_data and whale_data.moves %}
            {% for move in whale_data.moves %}
            <div class="card" style="border-left: 3px solid var(--neon-green);">
                <div class="data-row">
                    <span style="font-weight:bold;">🎯 {{ move.player }} ({{ move.sport }})</span>
                    <span class="neon-text">{{ move.action }}</span>
                </div>
                <div class="card-subtitle" style="margin-top:4px;">Line Target: {{ move.line }} | Public Resistance: <span class="highlight">{{ move.public_resistance }}</span></div>
                <div style="font-size:0.8rem; color:var(--sky-blue); font-weight:bold; margin-top:6px;">EVAL: {{ move.matrix_evaluation }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="card"><div class="card-subtitle" style="margin-bottom:0;">No whale movements tracked yet. Stream payload data to load.</div></div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, whale_data=load_data(), feeds=get_live_matrix_feeds())

@app.route('/api/matrix/update', methods=['POST'])
def update_matrix_data():
    try:
        payload = request.get_json()
        if not payload: return jsonify({"error": "No data"}), 400
        save_data(payload)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
