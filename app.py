import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DATA_FILE = "sports_data.json"

def get_live_matrix_feeds():
    """Reads live scraper updates from disk, or provides matching matrix structures."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
            
    # FALLBACK ENGINE SLATE DATA
    return [
        {
            "matchup": "Sam Houston State vs Liberty",
            "spread": "-13.5",
            "total": "52.5",
            "take_action": "TAKE: Sam Houston Alternate Pass Yards (MORE 175.0 Floor)",
            "context": "Current market context target: Williams Stadium • Line: Liberty -13.5 (O/U 52.5).",
            "syndicate_name": "Alpha Syndicate",
            "syndicate_size": "5x",
            "syndicate_market": "Sam Houston Pass Volume Sliders",
            "public_resistance": "94%",
            "evaluation": "ALPHA WHALE SIGNAL: HEAVY MISPRICING EXPOSED"
        }
    ]

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

        {% for game in games %}
        <!-- ⚡ AUTOMATED COMM SHEET SECTION -->
        <div class="section-header">⚡ LIVE AUTOMATED COMM SHEET</div>
        <div class="card automated-sheet">
            <div class="data-row">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE SPREAD RECON</span>
                <span class="neon-text">👉 {{ game.take_action }}</span>
            </div>
            <div class="card-subtitle" style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 8px;">{{ game.context }}</div>
            
            <div class="data-row" style="margin-top:12px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE OVER/UNDER RECON</span>
                <span class="neon-text">👉 Analyzing Pacing</span>
            </div>
            <div class="card-subtitle" style="font-size: 0.8rem; color: var(--text-dim); margin-top: 4px;">Will display exact live points threshold targets based on quarter pacing.</div>
        </div>

        <!-- 👁️ SYNDICATE CONSENSUS SECTION -->
        <div class="section-header">👁️ SYNDICATE CONSENSUS & SENTIMENT VOLATILITY</div>
        <div class="card">
            <div class="data-row">
                <div>
                    <div style="font-weight:bold;">{{ game.syndicate_name }}</div>
                    <div style="font-size:0.75rem; color:var(--text-dim);">Size: {{ game.syndicate_size }}</div>
                </div>
                <div style="text-align:right;">
                    <div class="blue-text" style="font-weight:bold;">{{ game.syndicate_market }}</div>
                    <div style="font-size:0.75rem; color:var(--alert-orange);">{{ game.public_resistance }} Public Resistance</div>
                </div>
            </div>
            <div class="data-row" style="margin-top:8px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <span style="font-weight:bold; color:var(--alert-orange);">🔍 EVALUATION:</span>
                <span class="highlight">{{ game.evaluation }}</span>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    games_data = get_live_matrix_feeds()
    return render_template_string(HTML_TEMPLATE, games=games_data)

@app.route("/update", methods=["POST"])
def update():
    try:
        incoming_data = request.get_json()
        if not incoming_data:
            return jsonify({"status": "error", "message": "Payload empty"}), 400
        
        with open(DATA_FILE, "w") as f:
            json.dump(incoming_data, f, indent=4)
        return jsonify({"status": "success", "message": "Matrix synced successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
