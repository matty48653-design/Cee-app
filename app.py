# Save this complete code file to replace your app.py folder
from flask import Flask, render_template_string
import time

app = Flask(__name__)

# System database injecting yesterday's false line traps and today's active loops
LIVE_SPORTS_DATA = {
    "last_update": f"{time.strftime('%I:%M %p')} EST",
    "ticker_lines": [
        "🏈 TONIGHT: Atlanta Falcons @ New Orleans Saints (8:15 PM ET) ",
        "🏒 NHL SLATE: Philadelphia Flyers @ Tampa Bay Lightning (7:00 PM ET) ",
        "🏒 NHL SLATE: Winnipeg Jets @ Pittsburgh Penguins (7:30 PM ET) ",
        "🏒 NHL SLATE: Ottawa Senators @ Boston Bruins (7:30 PM ET) ",
        "🏒 NHL SLATE: San Jose Sharks @ Dallas Stars (8:00 PM ET) ",
        "🎯 STRATEGY: TRACKING MILESTONES & UNDER FLOORS | ❌ MLB SUPPRESSED"
    ],
    "yesterday_traps": [
        {"game": "New England @ Buffalo", "final": "NE 29 - 26 BUF", "script": "Public Trap: Bills heavily backed at home. Sharp line dropping from -6.5 to -4.5 flagged a massive public execution layout. Result: Upset."},
        {"game": "Kansas City @ Las Vegas", "final": "KC 30 - 27 LV", "script": "Public Trap: Chiefs over-backed heavily by public volume. House inflated player milestones to force under value. Result: Safe Under floor hit."}
    ],
    "nfl_games": [
        {
            "matchup": "Atlanta Falcons @ New Orleans Saints",
            "time": "8:15 PM ET",
            "spread": "Saints -1.5 (Trap Flagged 🚨)",
            "live_status": {"period": "PRE-GAME", "clock": "00:00", "away_score": 0, "home_score": 0},
            "milestones": [
                {"player": "Bijan Robinson (RB)", "stat": "Over 50.5 Rush Yds", "status": "PREMIUM FLOOR"},
                {"player": "Michael Penix Jr. (QB)", "stat": "Over 200.5 Pass Yds", "status": "SHARP INTEGRITY"}
            ],
            "injury_tracker": {
                "severity_index": "CRITICAL DEFENSIVE DEFICIT",
                "players": [
                    {"name": "Kaden Elliss (LB)", "status": "OUT", "impact": "Front-Seven Depth Core Collapse"},
                    {"name": "Carl Granderson (DE)", "status": "OUT", "impact": "Pass Rush Containment Void"},
                    {"name": "Anfernee Jennings (DE)", "status": "OUT", "impact": "Knee injury sustained against Raiders; thins defensive edge rotation"},
                    {"name": "Pete Werner (LB)", "status": "QUESTIONABLE", "impact": "Shoulder injury; weakside speed limitations if active"}
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
            "live_status": {"period": "PRE-GAME", "clock": "20:00", "away_score": 0, "home_score": 0},
            "injury_tracker": {
                "severity_index": "LIGHTNING BLUELINE LIMIT",
                "players": [{"name": "Emil Lilleberg (D)", "status": "OUT", "impact": "Expected out 1 week; shakes up third pairing depth"}]
            }
        },
        {
            "matchup": "Winnipeg Jets @ Pittsburgh Penguins",
            "time": "7:30 PM ET",
            "type": "Total Goals",
            "line": "Under 6.5",
            "status": "SHARP UNDER FLOOD",
            "live_status": {"period": "PRE-GAME", "clock": "20:00", "away_score": 0, "home_score": 0},
            "injury_tracker": {
                "severity_index": "STABLE BENCHMARK FLOORS",
                "players": [{"name": "Connor Hellebuyck (G)", "status": "IR", "impact": "Stuart Skinner maintaining primary start volume"}]
            }
        }
    ]
}

SYSTEM_STATE = {
    "version": "5.7 Script-Archive",
    "status": "AWS Cloud Feed Matrix OK",
    "milestone_baseline": "20.00"
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Live Stream v5.7</title>
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
        .game-title { font-weight: 700; color: #FFFFFF; font-size: 14px; margin-bottom: 6px; display: flex; justify-content: space-between; }
        .game-time { color: #A1A1AA; font-size: 11px; font-weight: normal; }
        .trap-row { background: #1C1212; border: 1px solid #3D1A1A; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 12px; }
        .trap-title { font-weight: bold; color: #FF5252; display: flex; justify-content: space-between; margin-bottom: 4px; }
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
            <h3>⚠️ Yesterday's Script Trap Analysis</h3>
            {% for trap in feeds.yesterday_traps %}
            <div class="trap-row">
                <div class="trap-title"><span>🛑 {{ trap.game }}</span> <span style="color: #A1A1AA;">{{ trap.final }}</span></div>
                <div style="color: #E4E4E7; margin-top: 3px; line-height: 1.4;">{{ trap.script }}</div>
            </div>
            {% endfor %}
        </div>
        <div class="card">
            <h3>🏈 Active NFL Milestone Slate</h3>
            {% for game in feeds.nfl_games %}
            <div class="game-title"><span>{{ game.matchup }}</span><span class="game-time">{{ game.time }}</span></div>
            <div class="scoreboard-box">
                <div class="score-team-col"><span>ATL Falcons</span><span>NO Saints</span></div>
                <div class="score-num-col"><span>{{ game.live_status.away_score }}</span><span>{{ game.live_status.home_score }}</span></div>
                <div class="score-clock-col"><div class="clock-period">{{ game.live_status.period }}</div><div class="clock-time">{{ game.live_status.clock }}</div></div>
            </div>
            <div style="font-size: 12px; color: #EF4444; margin-bottom: 8px; font-weight: 600;">Market: {{ game.spread }}</div>
            {% for prop in game.milestones %}
            <div class="data-row"><span style="color: #FFFFFF; font-weight: 600;">{{ prop.player }}</span>: {{ prop.stat }}<span class="badge-premium">{{ prop.status }}</span></div>
            {% endfor %}
            <div class="injury-header">⚠️ MORALE DEFICIT STREAM: {{ game.injury_tracker.severity_index }}</div>
