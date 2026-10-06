# app.py - Complete v5.6 - Operational Tracking Engine (No Personal Slips)
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def dashboard():
    cfb_game = {
        "home": "Troy",
        "away": "Southern Miss",
        "status": "UPCOMING",
        "sliders": [
            {"player": "Landry Lyddy (USM)", "metric": "200+ Pass Yards", "target": "OVER", "yield": "77%"},
            {"player": "Goose Crowder (TROY)", "metric": "190+ Pass Yards", "target": "OVER", "yield": "72%"},
            {"player": "Jaheim Merriweather (TROY)", "metric": "40+ Rush Yards", "target": "OVER", "yield": "47%"}
        ]
    }
    
    nhl_games = [
        {"home": "Detroit Red Wings", "away": "Ottawa Senators", "angle": "Divisional Pivot", "play": "Ottawa ML (+115)", "handle": "71% Sharp Cash"},
        {"home": "Toronto Maple Leafs", "away": "Nashville Predators", "angle": "Public Trap Fade", "play": "Nashville ML (+130)", "handle": "87% Public on TOR"},
        {"home": "Seattle Kraken", "away": "Vegas Golden Knights", "angle": "Late Night Structure", "play": "Seattle ML (+142)", "handle": "Vegas Public Premium"}
    ]
    
    # House panic thresholds & structural tracking elements
    house_matrix = {
        "metrics": [
            {"name": "Panic Threshold Trigger", "id": "panic_trigger", "value": "0.0%", "color": "var(--text-muted)"},
            {"name": "Morale Deficit Stream", "id": "morale_deficit", "value": "Stable", "color": "var(--accent-green)"},
            {"name": "Line-Decay Manipulation Traps", "id": "decay_traps", "value": "Scanning...", "color": "var(--accent-orange)"}
        ]
    }
    
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, tracker=house_matrix)

@app.route('/api/feed')
def live_feed():
    return jsonify({
        "status": "Pipeline Active",
        "version": "5.6-Operational",
        "live_metrics": {
            "panic_trigger": {"value": "Active Scan", "color": "var(--accent-green)"},
            "morale_deficit": {"value": "Monitoring Kickoff", "color": "var(--text-muted)"},
            "decay_traps": {"value": "0 Flagged", "color": "var(--accent-green)"}
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
