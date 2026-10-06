# app.py - Complete v5.7 - Syndicate & Sharp Wallet Tracking Core
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
    
    # Sharp Money Group / Wallet Tracking Feed Data Structure
    syndicate_picks = {
        "groups": [
            {"alias": "Alpha Syndicate (ROI: +6.4%)", "target": "Southern Miss +10.5", "size": "5x Normal", "status": "Locked In", "color": "var(--accent-green)"},
            {"alias": "Wallet #4092 (High-Stakes NHL)", "target": "Nashville ML (+130)", "size": "3.5x Normal", "status": "Locked In", "color": "var(--accent-green)"},
            {"alias": "Vegas Sharp Box (Transition Fade)", "target": "Ottawa ML (+115)", "size": "2x Normal", "status": "Locked In", "color": "var(--accent-green)"}
        ]
    }
    
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, sharps=syndicate_picks)

@app.route('/api/feed')
def live_feed():
    """Live sharp data feed endpoint for background tracking updates."""
    return jsonify({
        "status": "Pipeline Active",
        "version": "5.7-Sharp-Tracer",
        "syndicate_updates": [
            {"alias": "Alpha Syndicate (ROI: +6.4%)", "target": "Southern Miss +10.5", "size": "5x Normal", "status": "Locked In", "color": "var(--accent-green)"},
            {"alias": "Wallet #4092 (High-Stakes NHL)", "target": "Nashville ML (+130)", "size": "3.5x Normal", "status": "Locked In", "color": "var(--accent-green)"},
            {"alias": "Vegas Sharp Box (Transition Fade)", "target": "Ottawa ML (+115)", "size": "2x Normal", "status": "Locked In", "color": "var(--accent-green)"}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
