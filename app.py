# app.py - Complete v5.8 - Syndicate Tracer + Sentiment Volatility + Early Board Map
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
    
    # 🎯 FEATURE 1 INTEGRATION: Syndicates paired with Sentiment Volatility Scores
    syndicate_picks = {
        "groups": [
            {"alias": "Alpha Syndicate", "target": "Southern Miss +10.5", "size": "5x", "volatility": "91% Resistance", "v_color": "#ff9100"},
            {"alias": "Wallet #4092 (High-Stakes)", "target": "Nashville ML (+130)", "size": "3.5x", "volatility": "84% Resistance", "v_color": "#ff9100"},
            {"alias": "Vegas Sharp Box", "target": "Ottawa ML (+115)", "size": "2x", "volatility": "68% Resistance", "v_color": "#00e676"}
        ]
    }
    
    # 🌅 FEATURE 2 INTEGRATION: Tomorrow Morning's Early Board Map
    early_board = {
        "slate_date": "Wednesday Morning Open",
        "games": [
            {"sport": "NFL", "matchup": "Detroit Lions vs. Green Bay Packers", "open_line": "Lions -3.5", "movement": "Locked"},
            {"sport": "NHL", "matchup": "Montreal Canadiens vs. Boston Bruins", "open_line": "Bruins ML (-165)", "movement": "Locked"},
            {"sport": "CFB", "matchup": "Western Michigan vs. Central Michigan", "open_line": "Over 54.5", "movement": "Locked"}
        ]
    }
    
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, sharps=syndicate_picks, early=early_board)

@app.route('/api/feed')
def live_feed():
    """Background engine update feed providing live shifts to the UI script."""
    return jsonify({
        "status": "Pipeline Active",
        "version": "5.8-Dual-Feature",
        "sentiment_updates": {
            "Alpha Syndicate": "94% Public Resistance",
            "Wallet #4092 (High-Stakes)": "87% Public Resistance",
            "Vegas Sharp Box": "69% Public Resistance"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
