from flask import Flask, render_template_string
import time

app = Flask(__name__)

LIVE_SPORTS_DATA = {
    "last_update": f"{time.strftime('%I:%M %p')} EST",
    "ticker_lines": [
        "🎯 BASELINE: 20.00 COMPOUNDING INCREMENTAL GROWTH",
        "🏈 NFL ALERT: SAINTS LINE DROP FROM -2.5 TO -1.5 -> SHARP MONEY FLOOD DETECTED",
        "🏒 NHL PROJECTION: DEFENSIVE UNDER-FLOORS VALUE DETECTED ACROSS 4-GAME TONIGHT SLATE",
        "❌ FILTER ACTIVE: MLB BASEBALL DATA CHANNELS COMPLETELY SUPPRESSED"
    ],
    "nfl_games": [
        {
            "matchup": "Atlanta Falcons @ New Orleans Saints",
            "time": "8:15 PM ET",
            "spread": "Saints -1.5 (Trap Flagged 🚨)",
            "milestones": [
                {"player": "Bijan Robinson (RB)", "stat": "Over 50.5 Rush Yds", "status": "PREMIUM FLOOR"},
                {"player": "Michael Penix Jr. (QB)", "stat": "Over 200.5 Pass Yds", "status": "SHARP INTEGRITY"}
            ],
            "injury_tracker": {
                "severity_index": "CRITICAL DEFENSIVE DEFICIT",
                "players": [
                    {"name": "Kaden Elliss (LB)", "status": "OUT", "impact": "Front-Seven Depth Core Collapse"},
                    {"name": "Carl Granderson (DE)", "status": "OUT", "impact": "Pass Rush Containment Void"},
                    {"name": "Pete Werner (LB)", "status": "QUESTIONABLE", "impact": "Weakside Speed Restrictions"}
                ]
            }
        }
    ],
    "nhl_games": [
        {
            "matchup": "Philadelphia Flyers @ Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "type": "Total Goals",
            "line": "Under 6.0",
            "status": "CONTRARIAN VALUE",
            "injury_tracker": {
                "severity_index": "LIGHTNING BLUELINE LIMIT",
                "players": [
                    {"name": "Emil Lilleberg (D)", "status": "OUT", "impact": "Expected out 1 week; shakes up third pairing depth"}
                ]
            }
        },
        {
            "matchup": "Winnipeg Jets @ Pittsburgh Penguins",
            "time": "7:30 PM ET",
            "type": "Total Goals",
            "line": "Under 6.5",
            "status": "SHARP UNDER FLOOD",
            "injury_tracker": {
                "severity_index": "STABLE BENCHMARK FLOORS",
                "players": [
                    {"name": "Connor Hellebuyck (G)", "status": "IR", "impact": "Stuart Skinner maintaining primary start volume"}
                ]
            }
        }
    ]
}

SYSTEM_STATE = {
    "version": "5.5 Live-Ticker-Stream",
    "status": "AWS Cloud Nodes Synchronized",
    "milestone_baseline": "20.00"
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Live Stream v5.5</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #0A0A0C; color: #E4E4E7; padding: 0; margin: 0; }
        .ticker-wrap { width: 100%; background: #16161F; border-bottom: 2px solid #00E676; overflow: hidden; padding: 8px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5); position: sticky; top: 0; z-index: 100; }
        .ticker { display: inline-block; white-space: nowrap; padding-left: 100%; animation: marquee 25s linear infinite; }
        .ticker-item { display: inline-block; padding: 0 25px; font-family: monospace; font-size: 12px; font-weight: bold; color: #00E676; letter-spacing: 0.5px; }
        @keyframes marquee { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-content { padding: 15px; }
        .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 10px; border-bottom: 2px solid #1F2937; margin-bottom: 15px; }
        .header h2 { margin: 0; color: #FFFFFF; font-size: 18px; font-weight: 800; letter-spacing: 0.5px; }
        .status-badge { background-color: rgba(0, 230, 118, 0.15); color: #00E676; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
        .card { background: #111115; border-radius: 12px; padding: 14px; margin-bottom: 15px; border: 1px solid #22222A; }
        .card h3 { margin: 0 0 12px 0; font-size: 13px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #1F2937; padding-bottom: 5px; }
        .game-title { font-weight: 700; color: #FFFFFF; font-size: 14px; margin-bottom: 8px; display: flex; justify-content: space-between; }
        .game-time { color: #A1A1AA; font-size: 11px; font-weight: normal; }
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
    <div class="ticker-wrap">
        <div class="ticker">
            {% for line in feeds.ticker_lines %}
            <div class="ticker-item">{{ line }}</div>
            {% endfor %}
        </div>
    </div>
    <div class="main-content">
        <div class="header">
            <h2>CEE CONTROLS v{{ state.version }}</h2>
            <div class="status-badge">ONLINE</div>
        </div>
        <div class="card">
            <h3>🏈 Active NFL Milestone Slate</h3>
            {% for game in feeds.nfl_games %}
            <div class="game-title"><span>{{ game.matchup }}</span><span class="game-time">{{ game.time }}</span></div>
            <div style="font-size: 12px; color: #EF4444; margin-bottom: 8px; font-weight: 600;">Market: {{ game.spread }}</div>
            {% endfor %}
            {% for game in feeds.nfl_games %}{% for prop in game.milestones %}
            <div class="data-row"><span style="color: #FFFFFF; font-weight: 600;">{{ prop.player }}</span>: {{ prop.stat }}<span class="badge-premium">{{ prop.status }}</span></div>
            {% endfor %}{% endfor %}
        </div>
        <div class="card">
            <h3><h3>🏒 Active NHL Contrarian Totals</h3>
            {% for game in feeds.nhl_games %}
            <div class="game-title" style="margin-bottom: 4px;"><span>{{ game.matchup }}</span><span class="game-time">{{ game.time }}</span></div>
            <div class="data-row" style="border-left: 3px solid #E040FB; margin-bottom: 8px;">
                <span style="color: #A1A1AA;">{{ game.type }}:</span> <strong style="color: #FFFFFF;">{{ game.line }}</strong>
                <span class="badge-premium" style="background: rgba(224, 64, 251, 0.12); color: #E040FB;">{{ game.status }}</span>
            </div>
            <div class="injury-header">🚨 SKATER ROSTER ATTRITION: {{ game.injury_tracker.severity_index }}</div>
            {% if game.injury_tracker.players %}{% for player in game.injury_tracker.players %}
            <div class="injury-row"><span style="color: #FFFFFF; font-weight: bold;">{{ player.name }}</span><span class="injury-status">{{ player.status }}</span><div class="injury-impact">Impact: {{ player.impact }}</div></div>
            {% endfor %}{% else %}<div style="font-size: 12px; color: #71717A; padding: 4px 10px;">No critical personnel constraints flagged.</div>{% endif %}
            <div style="margin-bottom: 15px;"></div>
            {% endfor %}
        </div>
        <div class="footer-text">Data pipeline channels refreshed at {{ feeds.last_update }}</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, feeds=LIVE_SPORTS_DATA, state=SYSTEM_STATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
