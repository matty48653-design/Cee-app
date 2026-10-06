# app.py - Complete v5.9 - Corrected Real-World Matchups & Syndicate Feed
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
    
    syndicate_picks = {
        "groups": [
            {"alias": "Alpha Syndicate", "target": "Southern Miss +10.5", "size": "5x", "volatility": "91% Resistance", "v_color": "#ff9100"},
            {"alias": "Wallet #4092 (High-Stakes)", "target": "Nashville ML (+130)", "size": "3.5x", "volatility": "84% Resistance", "v_color": "#ff9100"},
            {"alias": "Vegas Sharp Box", "target": "Ottawa ML (+115)", "size": "2x", "volatility": "68% Resistance", "v_color": "#00e676"}
        ]
    }
    
    # 🎯 CORRECTED REAL-WORLD WEEK 5 SLATE MATRIX
    early_board = {
        "slate_date": "Sunday Slate Open (Week 5)",
        "games": [
            {"sport": "NFL", "matchup": "Detroit Lions @ Arizona Cardinals", "open_line": "Lions -4.5", "movement": "Locked"},
            {"sport": "NFL", "matchup": "Chicago Bears @ Green Bay Packers", "open_line": "Bears -2.5", "movement": "Locked"},
            {"sport": "CFB", "matchup": "Western Michigan vs. Central Michigan", "open_line": "Over 54.5", "movement": "Locked"}
        ]
    }
    
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, sharps=syndicate_picks, early=early_board)

@app.route('/api/feed')
def live_feed():
    return jsonify({
        "status": "Pipeline Active",
        "version": "5.9-True-Slate",
        "sentiment_updates": {
            "Alpha Syndicate": "94% Public Resistance",
            "Wallet #4092 (High-Stakes)": "87% Public Resistance",
            "Vegas Sharp Box": "69% Public Resistance"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
