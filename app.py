import os
import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

# System database stream for your active slates
def get_live_matrix_feeds():
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
            "ticket_pct": 6,   # Crowd Count
            "handle_pct": 44,  # Real Cash
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
            "ticket_pct": 19,  # Crowd Count
            "handle_pct": 52,  # Real Cash
        }
    ]

# Integrated Frontend HTML Layout Template Structure
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
        <form method="POST" action="/">
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
                            <div style="font-size: 0.65rem; color: var(--text-dim);">👥 CROWD COUNT</div>
                            <div class="grid-val">{{ game.ticket_pct }}%</div>
                        </div>
                        <div>
                            <div style="font-size: 0.65rem; color: var(--text-dim);">💰 REAL CASH</div>
                            <div class="grid-val text-high">{{ game.handle_pct }}%</div>
                        </div>
                        <div>
                            <div style="font-size: 0.65rem; color: var(--text-dim);">📊 CASH GAP</div>
                            <div class="grid-val text-alert">+{{ gap }}%</div>
                        </div>
                    </div>
                    
                    <div style="font-size: 0.65rem; color: var(--text-dim); margin-top: 8px; line-height: 1.2;">
                        📍 Environment: {{ game.crowd_env }} <br>
                        ⚠️ {{ game.injury_notes }}
                    </div>
                </div>
            {% endfor %}

            <div class="footer-inputs">
                <div class="unit-input-box">
                    <label style="font-size: 0.8rem; font-weight: bold;">CEE Multiplier Level:</label>
                    <input type="number" name="unit_size" value="{{ unit_size }}" min="1" max="100">
                </div>
                <button type="submit" class="btn-update">RE-SCALE CALCULATOR</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    unit_size = 3
    if request.method == "POST":
        try:
            unit_size = int(request.form.get("unit_size", 3))
        except ValueError:
            unit_size = 3

    games_data = get_live_matrix_feeds()
    return render_template_string(HTML_TEMPLATE, games=games_data, unit_size=unit_size)

if __name__ == "__main__":
