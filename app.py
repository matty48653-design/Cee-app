from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Active Contrarian Edge Engine configuration filters
ALLOWED_SPORTS = ['NFL', 'CFB', 'NHL']
BLOCKED_MARKETS = ['puck_line', 'mlb']

def get_live_cee_feed():
    """
    Simulates the real-time Contrarian Edge Engine data pipeline.
    Pipes live game slates, flag traps, and active morale deficit streams
    directly into your frontend interface.
    """
    return {
        "nfl": {
            "matchup": "Atlanta Falcons @ New Orleans Saints",
            "time": "8:15 PM ET",
            "market_status": "Saints -1.5 (Trap Flagged 🚨)",
            "milestones": [
                {"player": "Bijan Robinson (RB)", "line": "Over 50.5 Rush Yds", "status": "PREMIUM FLOOR"},
                {"player": "Michael Penix Jr. (QB)", "line": "Over 200.5 Pass Yds", "status": "SHARP INTEGRITY"}
            ],
            "morale_deficit": [
                {"player": "Kaden Elliss (LB)", "status": "OUT", "impact": "Front-Seven Depth Core Collapse"},
                {"player": "Carl Granderson (DE)", "status": "OUT", "impact": "Pass Rush Containment Void"}
            ]
        },
        "nhl": {
            "matchup": "Philadelphia Flyers @ Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "market_status": "Money Line / Totals Only (Puck Line Blocked)",
            "status": "Scanning Money Flow..."
        }
    }

@app.route('/')
def index():
    data = get_live_cee_feed()
    
    # Generate player milestone rows dynamically
    nfl_milestone_rows = "".join([
        f"<tr><td><b>{m['player']}</b></td><td>{m['line']}</td><td><span class='status-tag sharp'>{m['status']}</span></td></tr>"
        for m in data['nfl']['milestones']
    ])
    
    # Generate morale deficit injury rows dynamically
    nfl_injury_rows = "".join([
        f"<tr><td><span class='status-tag out'>{i['player']}</span></td><td>{i['status']}</td><td>{i['impact']}</td></tr>"
        for i in data['nfl']['morale_deficit']
    ])

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CEE v5.3 Matrix</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; background-color: #0c0f12; color: #ffffff; padding: 16px; margin: 0; }}
            h1 {{ color: #00e676; font-size: 22px; margin-bottom: 4px; font-weight: 700; }}
            p {{ color: #888888; font-size: 14px; margin-top: 0; margin-bottom: 24px; }}
            .section-title {{ font-size: 14px; color: #ff5252; font-weight: bold; text-transform: uppercase; margin-top: 24px; margin-bottom: 8px; letter-spacing: 0.5px; }}
            .game-card {{ background-color: #14191f; border-radius: 8px; padding: 16px; margin-bottom: 16px; border: 1px solid #222b35; }}
            .game-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222b35; padding-bottom: 10px; margin-bottom: 10px; }}
            .matchup {{ font-weight: bold; font-size: 16px; }}
            .time {{ color: #888888; font-size: 12px; }}
            .market-alert {{ color: #ff5252; font-size: 13px; font-weight: bold; margin-bottom: 12px; }}
            .matrix-table {{ width: 100%; border-collapse: collapse; margin-top: 4px; }}
            .matrix-table th, .matrix-table td {{ padding: 10px; text-align: left; font-size: 13px; border-bottom: 1px solid #1c232b; }}
            .matrix-table th {{ color: #00e676; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #222b35; }}
            .status-tag {{ padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
            .status-tag.sharp {{ background-color: rgba(0, 230, 118, 0.1); color: #00e676; border: 1px solid #00e676; }}
            .status-tag.out {{ background-color: rgba(255, 82, 82, 0.1); color: #ff5252; border: 1px solid #ff5252; }}
        </style>
    </head>
    <body>
        <h1>Contrarian Edge Engine</h1>
        <p>v5.3 • Clean Table Matrix Active</p>
        
        <div class="section-title">🏈 Active NFL Milestone Slate</div>
        <div class="game-card">
            <div class="game-header">
                <span class="matchup">{data['nfl']['matchup']}</span>
                <span class="time">{data['nfl']['time']}</span>
            </div>
            <div class="market-alert">Market: {data['nfl']['market_status']}</div>
            <table class="matrix-table">
                <thead>
                    <tr><th>Player</th><th>Target Milestone</th><th>Integrity</th></tr>
                </thead>
                <tbody>
                    {nfl_milestone_rows}
                </tbody>
            </table>
            
            <div class="section-title" style="font-size: 11px; margin-top: 16px;">⚠️ Morale Deficit Stream: Critical Defensive Deficit</div>
            <table class="matrix-table">
                <tbody>
                    {nfl_injury_rows}
                </tbody>
            </table>
        </div>

        <div class="section-title">🏒 Active NHL Contrarian Totals</div>
        <div class="game-card">
            <div class="game-header">
                <span class="matchup">{data['nhl']['matchup']}</span>
                <span class="time">{data['nhl']['time']}</span>
            </div>
            <div class="market-alert" style="color: #00e676;">{data['nhl']['market_status']}</div>
            <div style="font-size: 13px; color: #888888;">Status: {data['nhl']['status']}</div>
        </div>
    </body>
    </html>
    """

@app.route('/api/matrix')
def matrix_api():
    return jsonify(get_live_cee_feed())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
