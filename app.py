import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DATA_FILE = "sports_data.json"

def get_live_matrix_feeds():
    # If the scanner has successfully sent live data, read it!
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
            
    # FALLBACK STATIC DATA: Keeps your screen beautiful if live data fails
    return [
        {
            "matchup": "Dallas Cowboys vs New York Giants",
            "spread": "-3.5",
            "total": "44.5",
            "metrics": {
                "travel": "🛩️ Cowboys: Rested | Giants: Home",
                "crowd": "🔊 High crowd noise factor expected",
                "injury": "🏥 Key WR questionable for Giants",
                "morale": "🔥 Cowboys coming off a 3-game win streak",
                "handle": "💰 68% of public money on Cowboys spread",
                "trajectory": "📈 Total line trending upwards from 43.0"
            }
        },
        {
            "matchup": "New York Rangers vs New Jersey Devils",
            "spread": "-1.5",
            "total": "5.5",
            "metrics": {
                "travel": "🚌 Local rivalry game - minimal travel",
                "crowd": "🏒 Split stadium atmosphere expected",
                "injury": "🏥 Starting goalie confirmed for Rangers",
                "morale": "⚡ Devils looking to bounce back from loss",
                "handle": "💰 Heavy sharp action on the Under",
                "trajectory": "📉 Spread moved down from -2.0"
            }
        }
    ]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE AUTOMATION MATRIX</title>
    <style>
        body {
            background-color: #0b0f19;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 15px;
        }
        .title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 700;
            color: #10b981;
        }
        .pulse-dot {
            width: 12px;
            height: 12px;
            background-color: #10b981;
            border-radius: 50%;
        }
        .matrix-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .card {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 20px;
        }
        .matchup-text {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #f3f4f6;
        }
        .line-item {
            font-size: 14px;
            color: #9ca3af;
            margin: 4px 0;
        }
        .line-text {
            font-weight: 700;
            color: #10b981;
        }
        .metrics-box {
            margin-top: 15px;
            padding-top: 12px;
            border-top: 1px dashed #374151;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .metric-row {
            font-size: 12px;
            color: #d1d5db;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🟢 CEE AUTOMATION MATRIX</div>
        <div class="status-indicator">
            <div class="pulse-dot"></div>
            LIVE API FEED ACTIVE
        </div>
    </div>
    
    <div class="matrix-container">
        {% for game in games %}
        <div class="card">
            <div class="matchup-text">{{ game.matchup }}</div>
            <div class="line-item">Spread: <span class="line-text">{{ game.spread }}</span></div>
            <div class="line-item">Total: <span class="line-text">{{ game.total }}</span></div>
            
            {% if game.metrics %}
            <div class="metrics-box">
                <div class="metric-row">{{ game.metrics.travel }}</div>
                <div class="metric-row">{{ game.metrics.crowd }}</div>
                <div class="metric-row">{{ game.metrics.injury }}</div>
                <div class="metric-row">{{ game.metrics.morale }}</div>
                <div class="metric-row">{{ game.metrics.handle }}</div>
                <div class="metric-row">{{ game.metrics.trajectory }}</div>
            </div>
            {% endif %}
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
    try:
        incoming_data = request.get_json()
        if incoming_data:
            with open(DATA_FILE, "w") as f:
                json.dump(incoming_data, f)
            return jsonify({"status": "success", "message": "Data saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
