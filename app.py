# Save this complete code file to replace your app.py folder
from flask import Flask, render_template_string, jsonify
import time

app = Flask(__name__)

# Live Data Feed Simulator structured exactly like our real-world background scraper
LIVE_SPORTS_DATA = {
    "last_update": f"{time.strftime('%I:%M %p')} EST",
    "nfl_games": [
        {
            "matchup": "Atlanta Falcons @ New Orleans Saints",
            "time": "8:15 PM ET",
            "spread": "Saints -1.5 (Trap Flagged 🚨)",
            "milestones": [
                {"player": "Bijan Robinson (RB)", "stat": "Over 50.5 Rush Yds", "status": "PREMIUM FLOOR"},
                {"player": "Michael Penix Jr. (QB)", "stat": "Over 200.5 Pass Yds", "status": "SHARP INTEGRITY"}
            ]
        }
    ],
    "nhl_games": [
        {
            "matchup": "Philadelphia Flyers @ Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "type": "Total Goals",
            "line": "Under 6.0",
            "status": "CONTRARIAN VALUE"
        },
        {
            "matchup": "Winnipeg Jets @ Pittsburgh Penguins",
            "time": "7:30 PM ET",
            "type": "Total Goals",
            "line": "Under 6.5",
            "status": "SHARP UNDER FLOOD"
        }
    ]
}

SYSTEM_STATE = {
    "version": "5.2 Data-Stream",
    "status": "Feeds Synchronized",
    "milestone_baseline": "20.00"
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Live Stream v5.2</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #0A0A0C; color: #E4E4E7; padding: 15px; margin: 0; }
        .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 10px; border-bottom: 2px solid #1F2937; margin-bottom: 15px; }
        .header h2 { margin: 0; color: #00E676; font-size: 18px; font-weight: 800; letter-spacing: 0.5px; }
        .status-badge { background-color: rgba(0, 230, 118, 0.15); color: #00E676; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
        .card { background: #111115; border-radius: 12px; padding: 14px; margin-bottom: 15px; border: 1px solid #22222A; }
        .card h3 { margin: 0 0 12px 0; font-size: 13px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #1F2937; padding-bottom: 5px; }
        .game-title { font-weight: 700; color: #FFFFFF; font-size: 14px; margin-bottom: 8px; display: flex; justify-content: space-between; }
        .game-time { color: #A1A1AA; font-size: 11px; font-weight: normal; }
        .data-row { background: #16161F; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 3px solid #00B0FF; }
        .data-row:last-child { margin-bottom: 0; }
        .badge-premium { background: rgba(0, 230, 118, 0.12); color: #00E676; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; float: right; }
        .footer-text { text-align: center; color: #71717A; font-size: 11px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>CEE REAL-TIME DATA v{{ state.version }}</h2>
        <div class="status-badge">SYNCED</div>
    </div>

    <!-- NFL DATA STREAM CARD -->
    <div class="card">
        <h3>🏈 Active NFL Milestone Slate</h3>
        {% for game in feeds.nfl_games %}
        <div class="game-title">
            <span>{{ game.matchup }}</span>
            <span class="game-time">{{ game.time }}</span>
        </div>
        <div style="font-size: 12px; color: #EF4444; margin-bottom: 8px; font-weight: 600;">Market: {{ game.spread }}</div>
        {% endfor %}
        
        {% for game in feeds.nfl_games %}
            {% for prop in game.milestones %}
            <div class="data-row">
                <span style="color: #FFFFFF; font-weight: 600;">{{ prop.player }}</span>: {{ prop.stat }}
                <span class="badge-premium">{{ prop.status }}</span>
            </div>
            {% endfor %}
        {% endfor %}
    </div>

    <!-- NHL DATA STREAM CARD -->
    <div class="card">
        <h3>🏒 Active NHL Contrarian Totals</h3>
        {% for game in feeds.nhl_games %}
        <div class="game-title" style="margin-bottom: 4px;">
            <span>{{ game.matchup }}</span>
            <span class="game-time">{{ game.time }}</span>
        </div>
        <div class="data-row" style="border-left: 3px solid #E040FB; margin-bottom: 12px;">
            <span style="color: #A1A1AA;">{{ game.type }}:</span> <strong style="color: #FFFFFF;">{{ game.line }}</strong>
            <span class="badge-premium" style="background: rgba(224, 64, 251, 0.12); color: #E040FB;">{{ game.status }}</span>
        </div>
        {% endfor %}
    </div>

    <div class="footer-text">Data pipeline channels refreshed at {{ feeds.last_update }}</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, feeds=LIVE_SPORTS_DATA, state=SYSTEM_STATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
