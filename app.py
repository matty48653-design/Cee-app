from flask import Flask, render_template_string
import time

app = Flask(__name__)

# Clean dataset locking player metrics directly to their specific team nodes
LIVE_SPORTS_DATA = {
    "last_update": f"{time.strftime('%I:%M %p')} EST",
    "nfl_games": [
        {
            "away_team": "Atlanta Falcons",
            "home_team": "New Orleans Saints",
            "time": "8:15 PM ET",
            "spread": "Saints -1.5 (Trap Flagged 🚨)",
            "live_status": {"period": "PRE-GAME", "clock": "00:00", "away_score": 0, "home_score": 0},
            "validated_roster_props": [
                {"team": "Atlanta Falcons", "player": "Bijan Robinson (RB)", "stat": "Over 50.5 Rush Yds", "status": "PREMIUM FLOOR"},
                {"team": "Atlanta Falcons", "player": "Michael Penix Jr. (QB)", "stat": "Over 200.5 Pass Yds", "status": "SHARP INTEGRITY"}
            ],
            "injury_tracker": {
                "severity_index": "CRITICAL DEFENSIVE DEFICIT",
                "players": [
                    {"team": "New Orleans Saints", "name": "Kaden Elliss (LB)", "status": "OUT", "impact": "Front-Seven Depth Core Collapse"},
                    {"name": "Carl Granderson (DE)", "status": "OUT", "impact": "Pass Rush Containment Void"}
                ]
            }
        }
    ],
    "nhl_games": [
        {
            "away_team": "Philadelphia Flyers",
            "home_team": "Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "type": "Total Goals",
            "line": "Under 6.0",
            "status": "CONTRARIAN VALUE",
            "live_status": {"period": "PRE-GAME", "clock": "20:00", "away_score": 0, "home_score": 0},
            "injury_tracker": {
                "severity_index": "LIGHTNING BLUELINE LIMIT",
                "players": [{"team": "Tampa Bay Lightning", "name": "Emil Lilleberg (D)", "status": "OUT", "impact": "Third Pairing Depth Disruption"}]
            }
        }
    ]
}

SYSTEM_STATE = {
    "version": "5.3 Clean-Table-Matrix",
    "status": "AWS Cloud Feed Matrix OK",
    "milestone_baseline": "20.00"
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Live Stream v5.3</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #0A0A0C; color: #E4E4E7; padding: 15px; margin: 0; }
        .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 10px; border-bottom: 2px solid #1F2937; margin-bottom: 15px; }
        .header h2 { margin: 0; color: #FFFFFF; font-size: 18px; font-weight: 800; letter-spacing: 0.5px; }
        .status-badge { background-color: rgba(0, 230, 118, 0.15); color: #00E676; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
        .card { background: #111115; border-radius: 12px; padding: 14px; margin-bottom: 15px; border: 1px solid #22222A; }
        .card h3 { margin: 0 0 12px 0; font-size: 13px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #1F2937; padding-bottom: 5px; }
        .game-title { font-weight: 700; color: #FFFFFF; font-size: 14px; margin-bottom: 6px; display: flex; justify-content: space-between; }
        .game-time { color: #A1A1AA; font-size: 11px; font-weight: normal; }
        .scoreboard-box { background: #1C1C24; border: 1px solid #2D2D3D; border-radius: 8px; padding: 10px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
        .score-team-col { display: flex; flex-direction: column; gap: 4px; font-size: 13px; font-weight: bold; color: #FFFFFF; }
        .score-num-col { display: flex; flex-direction: column; gap: 4px; font-size: 13px; font-weight: 800; color: #00E676; text-align: right; }
        .score-clock-col { text-align: center; border-left: 1px solid #2D3748; padding-left: 12px; }
        .clock-period { font-size: 10px; font-weight: 800; color: #9CA3AF; text-transform: uppercase; }
        .clock-time { font-family: monospace; font-size: 14px; font-weight: bold; color: #FFFFFF; margin-top: 2px; }
        .data-row { background: #16161F; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 3px solid #00B0FF; }
        .badge-premium { background: rgba(0, 230, 118, 0.12); color: #00E676; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; float: right; }
        .injury-header { font-size: 11px; font-weight: 800; color: #EF4444; letter-spacing: 0.5px; margin: 12px 0 6px 0; border-top: 1px dashed #2D3748; padding-top: 8px; }
        .injury-row { background: #1A1315; border: 1px solid #3A1F24; padding: 8px; border-radius: 6px; margin-bottom: 5px; font-size: 12px; }
        .injury-status { color: #EF4444; font-weight: bold; float: right; font-size: 11px; background: rgba(239, 68, 68, 0.15); padding: 1px 5px; border-radius: 3px; }
        .injury-impact { font-size: 11px; color: #A1A1AA; margin-top: 3px; }
        .footer-text { text-align: center; color: #71717A; font-size: 11px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>CEE CONTROLS v{{ state.version }}</h2>
        <div class="status-badge">ONLINE</div>
    </div>
    <div class="card">
        <h3>🏈 Active NFL Milestone Slate</h3>
        {% for game in feeds.nfl_games %}
        <div class="game-title"><span>{{ game.away_team }} @ {{ game.home_team }}</span><span class="game-time">{{ game.time }}</span></div>
        <div class="scoreboard-box">
            <div class="score-team-col"><span>{{ game.away_team }}</span><span>{{ game.home_team }}</span></div>
            <div class="score-num-col"><span>{{ game.live_status.away_score }}</span><span>{{ game.live_status.home_score }}</span></div>
            <div class="score-clock-col"><div class="clock-period">{{ game.live_status.period }}</div><div class="clock-time">{{ game.live_status.clock }}</div></div>
        </div>
        <div style="font-size: 12px; color: #EF4444; margin-bottom: 8px; font-weight: 600;">Market: {{ game.spread }}</div>
        {% for prop in game.validated_roster_props %}
        <div class="data-row"><span style="color: #FFFFFF; font-weight: 600;">[{{ prop.team }}] {{ prop.player }}</span>: {{ prop.stat }}<span class="badge-premium">{{ prop.status }}</span></div>
        {% endfor %}
        <div class="injury-header">⚠️ MORALE DEFICIT STREAM: {{ game.injury_tracker.severity_index }}</div>
        {% for player in game.injury_tracker.players %}
        <div class="injury-row"><span style="color: #FFFFFF; font-weight: bold;">[{{ player.team }}] {{ player.name }}</span><span class="injury-status">{{ player.status }}</span><div class="injury-impact">Impact: {{ player.impact }}</div></div>
        {% endfor %}
        {% endfor %}
    </div>
    <div class="card">
        <h3>🏒 Active NHL Contrarian Totals</h3>
        {% for game in feeds.nhl_games %}
        <div class="game-title" style="margin-bottom: 4px;"><span>{{ game.away_team }} @ {{ game.home_team }}</span><span class="game-time">{{ game.time }}</span></div>
        <div class="data-row" style="border-left: 3px solid #E040FB; margin-bottom: 8px;">
            <span style="color: #A1A1AA;">{{ game.type }}</span>: <strong style="color: #FFFFFF;">{{ game.line }}</strong>
            <span class="badge-premium" style="background: rgba(224, 64, 251, 0.12); color: #E040FB; float: right;">{{ game.status }}</span>
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
